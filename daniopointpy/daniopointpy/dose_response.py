import argparse

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import t

# Define different model functions
def linear_model(x, slope, intercept):
    return slope * x + intercept

def logistic_2p(x, EC50, slope):
    return 1 / (1 + np.exp((EC50 - x) * slope))

def logistic_3p(x, top, EC50, slope):
    return top / (1 + np.exp((EC50 - x) * slope))

def logistic_4p(x, top, bottom, EC50, slope):
    return bottom + (top - bottom) / (1 + np.exp((EC50 - x) * slope))

def calculate_ec50(params, model_type):
    if model_type in ["logistic_2p", "logistic_3p", "logistic_4p"]:
        return params[1]  # Assuming EC50 is the second parameter for these models
    else:
        return None

# Function to calculate the Jacobian matrix using finite differences
def jacobian(x, model, params, epsilon=1e-6):
    jac = np.zeros((len(x), len(params)))
    for i in range(len(params)):
        params1 = np.array(params, copy=True)
        params2 = np.array(params, copy=True)
        params1[i] += epsilon
        params2[i] -= epsilon
        f1 = model(x, *params1)
        f2 = model(x, *params2)
        jac[:, i] = (f1 - f2) / (2 * epsilon)
    return jac

# Function to predict with confidence intervals using the Jacobian matrix
def predict_with_confidence_interval(model_func, x, params, cov, alpha=0.05):
    pred = model_func(x, *params)
    jac = jacobian(x, model_func, params)
    se = np.sqrt(np.diag(np.dot(np.dot(jac, cov), jac.T)))
    t_stat = t.ppf(1 - alpha / 2., len(x) - len(params))
    ci_lower = pred - t_stat * se
    ci_upper = pred + t_stat * se
    return pred, ci_lower, ci_upper

# Function to fit the model and plot
def fit_and_plot(dose, response, model_type, output_file, initial_guesses=None, min_response=0, max_response=1):
    if model_type == "linear":
        model_func = linear_model
        params, cov = curve_fit(model_func, dose, response, p0=initial_guesses)
    elif model_type == "logistic_2p":
        model_func = logistic_2p
        params, cov = curve_fit(model_func, dose, response, p0=initial_guesses)
    elif model_type == "logistic_3p":
        model_func = lambda x, EC50, slope: logistic_3p(x, max_response, EC50, slope)
        params, cov = curve_fit(model_func, dose, response, p0=initial_guesses)
    elif model_type == "logistic_4p":
        model_func = lambda x, EC50, slope: logistic_4p(x, max_response, min_response, EC50, slope)
        params, cov = curve_fit(model_func, dose, response, p0=initial_guesses)
    else:
        raise ValueError("Invalid model type selected.")

    x_values = np.linspace(min(dose), max(dose), 200)
    pred, ci_lower, ci_upper = predict_with_confidence_interval(model_func, x_values, params, cov)

    ec50 = calculate_ec50(params, model_type)

    # Plot the data and the fitted model with confidence intervals
    plt.figure(figsize=(8, 5))
    plt.scatter(dose, response, color='red', label='Data')
    plt.plot(x_values, pred, 'b-', label=f'Fitted {model_type} model')
    plt.fill_between(x_values, ci_lower, ci_upper, color='blue', alpha=0.2, label='95% Confidence Interval')
    plt.title(f'Fitted {model_type.capitalize()} Curve with Confidence Interval')
    plt.xlabel('Dose')
    plt.ylabel('Response')
    plt.legend()
    plt.grid(True)

    plot_file_path = output_file.rsplit('.', 1)[0] + "_dose_response_curve.png"
    plt.savefig(plot_file_path)
    plt.close()

    # Save the summary to a file
    with open(output_file, 'w') as f:
        for i, param in enumerate(params):
            f.write(f"Parameter {i + 1}: {param:.4f}\n")
        if ec50 is not None:
            f.write(f"EC50: {ec50:.4f}\n")


# Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fit a selected model to dose-response data from a file and output statistics.")
    parser.add_argument("--file", type=str, required=True,
                        help="Path to the txt file with dose and response data. The file should contain two columns: dose and response.")
    parser.add_argument("--output_file", type=str, required=True,
                        help="Path to the output file for statistical results.")
    parser.add_argument("--model_type", type=str, required=True,
                        choices=["linear", "logistic_2p", "logistic_3p", "logistic_4p"],
                        help="The type of model to fit: linear, logistic_2p, logistic_3p, logistic_4p.")
    parser.add_argument("--min_response", type=float, default=0,
                        help="Minimum response value for fitting (only used for logistic_4p).")
    parser.add_argument("--max_response", type=float, default=1,
                        help="Maximum response value for fitting (used for logistic_3p and logistic_4p).")
    parser.add_argument("--initial_guesses", nargs='+', type=float, help="Initial guesses for the model parameters.")

    args = parser.parse_args()

    # Load dose and response data from the file
    data = np.loadtxt(args.file)
    dose = data[:, 0]
    response = data[:, 1]

    # Call the fit and plot function and save statistics
    fit_and_plot(dose, response, args.model_type, args.output_file, args.initial_guesses, args.min_response,
                 args.max_response)
