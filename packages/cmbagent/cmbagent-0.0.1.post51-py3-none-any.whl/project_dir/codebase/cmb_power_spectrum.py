# filename: codebase/cmb_power_spectrum.py
import camb
import numpy as np
import matplotlib.pyplot as plt
import time

# Set the database path for saving the plot
database_path = 'data/'


def compute_cmb_power_spectrum():
    """
    Computes the CMB temperature power spectrum using the CAMB package.

    Returns:
        l (numpy.ndarray): Multipole moments.
        cltt (numpy.ndarray): CMB temperature power spectrum.
    """
    # Initialize the CAMB parameters
    params = camb.CAMBparams()
    params.set_cosmology(H0=70, ombh2=0.022, omch2=0.12)
    params.InitPower.set_params(ns=0.965, r=0.0)
    params.set_for_lmax(2500)  # Set maximum multipole
    params.Want_CMB_lensing = True  # Enable lensing

    # Compute the power spectrum
    results = camb.get_results(params)
    power_spectra = results.get_cmb_power_spectra(params, CMB_unit='muK')
    l = np.arange(power_spectra['total'].shape[0])
    cltt = power_spectra['total'][:, 0]  # Extract TT spectrum

    return l, cltt


def plot_cmb_power_spectrum(l, cltt):
    """
    Plots the CMB temperature power spectrum.

    Parameters:
        l (numpy.ndarray): Multipole moments.
        cltt (numpy.ndarray): CMB temperature power spectrum.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(l, cltt, label='CMB Temperature Power Spectrum', color='blue')
    plt.xlabel('Multipole Moment (l)', fontsize=14)
    plt.ylabel('C_l (\u00B5K\u00B2)', fontsize=14)
    plt.title('CMB Temperature Power Spectrum', fontsize=16)
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # Save the plot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    plt.savefig(database_path + 'cmb_power_spectrum_1_' + timestamp + '.png', dpi=300)
    print("CMB temperature power spectrum plot saved as: cmb_power_spectrum_1_" + timestamp + ".png")


# Main execution
l, cltt = compute_cmb_power_spectrum()
plot_cmb_power_spectrum(l, cltt)