import logging
from typing import TYPE_CHECKING

import lal
import pandas as pd
import torch
from amplfi.utils.result import AmplfiResult
from ml4gw.transforms import ChannelWiseScaler

if TYPE_CHECKING:
    from amplfi.train.architectures.flows.base import FlowArchitecture
    from ml4gw.transforms import SpectralDensity, Whiten


def filter_samples(samples, parameter_sampler, inference_params):
    net_mask = torch.ones(samples.shape[0], dtype=bool)
    priors = parameter_sampler.priors
    for i, param in enumerate(inference_params):
        prior = priors[param]
        curr_samples = samples[:, i]
        log_probs = prior.log_prob(curr_samples)
        mask = log_probs == float("-inf")

        logging.debug(
            f"Removed {mask.sum()}/{len(mask)} samples for parameter "
            f"{param} outside of prior range"
        )

        net_mask &= ~mask

    logging.debug(
        f"Removed {(~net_mask).sum()}/{len(net_mask)} total samples "
        f"outside of prior range"
    )
    samples = samples[net_mask]
    return samples


def run_amplfi(
    amplfi_strain,
    amplfi_psd_strain,
    samples_per_event: int,
    spectral_density: "SpectralDensity",
    amplfi_whitener: "Whiten",
    amplfi: "FlowArchitecture",
    std_scaler: "ChannelWiseScaler",
    device: torch.device,
):
    # get pe data from the buffer and whiten it
    amplfi_psd_strain = amplfi_psd_strain.to(device)
    amplfi_strain = amplfi_strain.to(device)[None]
    psd = spectral_density(amplfi_psd_strain)[None]
    whitened = amplfi_whitener(amplfi_strain, psd)

    # construct and bandpass asd
    freqs = torch.fft.rfftfreq(
        whitened.shape[-1], d=1 / amplfi_whitener.sample_rate
    )
    num_freqs = len(freqs)
    psd = torch.nn.functional.interpolate(
        psd, size=(num_freqs,), mode="linear"
    )

    mask = freqs > amplfi_whitener.highpass
    if amplfi_whitener.lowpass is not None:
        mask *= freqs < amplfi_whitener.lowpass

    psd = psd[:, :, mask]
    asds = torch.sqrt(psd)

    # sample from the model and descale back to physical units
    logging.debug("Starting sampling")
    samples = amplfi.sample(samples_per_event, context=(whitened, asds))
    samples = samples.squeeze(1)
    logging.debug("Descaling samples")
    samples = samples.transpose(1, 0)
    descaled_samples = std_scaler(samples, reverse=True)
    descaled_samples = descaled_samples.transpose(1, 0)
    logging.debug("Finished AMPLFI")

    return descaled_samples


def postprocess_samples(
    samples: torch.Tensor,
    event_time: float,
    inference_params: list[str],
    parameter_sampler: torch.nn.Module,
) -> AmplfiResult:
    """
    Process samples into a bilby Result object
    that can be used for all downstream tasks
    """
    samples = filter_samples(samples, parameter_sampler, inference_params)

    phi_idx = inference_params.index("phi")
    dec_idx = inference_params.index("dec")
    ra = torch.remainder(
        lal.GreenwichMeanSiderealTime(event_time) + samples[..., phi_idx],
        torch.as_tensor(2 * torch.pi),
    )
    dec = samples[..., dec_idx]

    # build bilby posterior object for
    # parameters we want to keep
    posterior_params = ["chirp_mass", "mass_ratio", "distance"]

    posterior = {}
    for param in posterior_params:
        idx = inference_params.index(param)
        posterior[param] = samples.T[idx].flatten()

    # TODO remove
    posterior["phi"] = ra
    posterior["ra"] = ra
    posterior["dec"] = dec
    posterior = pd.DataFrame(posterior)

    result = AmplfiResult(
        label=f"{event_time}",
        posterior=posterior,
        search_parameter_keys=inference_params,
    )
    return result
