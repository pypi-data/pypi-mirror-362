import numpy as np
from normtransform import pytrans
from scipy.stats import probplot, norm
import matplotlib.pyplot as plt

def run_logsinh_demo(data, lcens, rcens, test_name, plot=True):
    """Run a left-censored log-sinh transformation demo with visualization."""
    print(f"\n==== {test_name} ====\n")

    # --- Step 1: Rescale data to stabilize estimation ---
    scaling = 5.0 / np.maximum(np.max(data), lcens)
    transform = pytrans.PyLogSinh(trans_lambda=1.0, trans_epsilon=1e-10, scale=scaling)

    print(f"Data shape: {data.shape}")
    print(f"Left censoring threshold: {lcens}")
    print(f"Right censoring threshold: {rcens}")

    rescaled_data = transform.rescale_many(data)
    rescaled_lcens = transform.rescale_one(lcens)
    rescaled_rcens = transform.rescale_one(rcens)

    # --- Step 2: Fit model using MAP estimation ---
    transform.optim_paramsSCE(rescaled_data, rescaled_lcens, rescaled_rcens, do_rescale=False, is_map=True)
    mu, sigma = transform.get_distribution_params()[2:4]

    # --- Step 3: Transform original data to normal space ---
    trans_data = transform.transform_many(rescaled_data)

    # --- Step 4: Generate bootstrap inverse-transformed samples ---
    inv_samples = []
    for _ in range(100):
        boot_sample = np.random.normal(mu, sigma, size=len(data))
        inv = transform.inv_rescale_many(transform.inv_transform_many(boot_sample))
        inv_samples.append(np.sort(inv))

    inv_samples = np.array(inv_samples)
    inv_p50 = np.percentile(inv_samples, 50, axis=0)
    inv_lo = np.percentile(inv_samples, 5, axis=0)
    inv_hi = np.percentile(inv_samples, 95, axis=0)

    # --- Step 5: Plot results...
    if plot:
        plot_results(data, transform, rescaled_lcens, mu, sigma, trans_data, inv_samples, inv_p50, inv_lo, inv_hi)
    return trans_data

def plot_results(data, transform, rescaled_lcens, mu, sigma, trans_data, inv_samples, inv_p50, inv_lo, inv_hi):
    plt.figure(figsize=(10, 7))
    ylim = (-1, 5)

    # 1. Q-Q Plot of Original Data
    plt.subplot(2, 2, 1)
    probplot(data, dist="norm", plot=plt)
    plt.ylim(ylim)
    plt.title("Q-Q Plot: Original Data")

    # 2. Q-Q Plot of One Inverse Sample
    plt.subplot(2, 2, 2)
    probplot(inv_samples[0], dist="norm", plot=plt)
    plt.ylim(ylim)
    plt.title("Q-Q Plot: Inverse-Transformed Sample")

    # 3. Observed vs. Inverse Sample Median + 90% Interval
    plt.subplot(2, 2, 3)
    plt.fill_between(np.sort(data), inv_lo, inv_hi, alpha=0.5, color="skyblue", label="90% Band")
    plt.scatter(np.sort(data), inv_p50, s=6, label="Median", color="blue")
    plt.plot(ylim, ylim, 'k--', label="1:1 Line")
    plt.xlabel("Observed Quantiles")
    plt.ylabel("Sample Quantiles")
    plt.title("Observed vs Inverse-Transformed")
    plt.legend()

    # 4. Histogram of Transformed Data with Fitted PDF
    plt.subplot(2, 2, 4)
    x_vals = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 200)
    pdf_vals = norm.pdf(x_vals, loc=mu, scale=sigma)

    plt.hist(trans_data, bins=30, density=True, alpha=0.6, color='gray', label="Transformed Data")
    plt.plot(x_vals, pdf_vals, 'r-', lw=2, label="Fitted Normal PDF")
    plt.xlabel("Transformed Normal Scale")
    plt.ylabel("Density")
    plt.title("Histogram + Fitted PDF")
    plt.legend()

    # Optional: Check mean of transformed data vs samples
    boot_sample_clipped = np.random.normal(mu, sigma, size=len(data))
    clip_thresh = transform.transform_one(rescaled_lcens)
    boot_sample_clipped[boot_sample_clipped < clip_thresh] = clip_thresh
    print(f"Mean (transformed data): {np.mean(trans_data):.3f}")
    print(f"Mean (boot sample): {np.mean(boot_sample_clipped):.3f}")

    plt.tight_layout()
    plt.show()

# ==== Example Run ====
if __name__ == "__main__":
    np.random.seed(10)

    # Simulated example with left-censored gamma data
    LEFT_CENS = 0.0
    RIGHT_CENS = 999.0

    # Generate gamma data and apply left censoring
    raw_data = np.random.gamma(shape=1.5, scale=0.5, size=1000)
    shifted_data = raw_data - np.percentile(raw_data, 10)
    censored_data = np.maximum(shifted_data, LEFT_CENS)
    plot_results = True
    run_logsinh_demo(censored_data, LEFT_CENS, RIGHT_CENS, "Log-Sinh with Left Censoring", plot_results)
