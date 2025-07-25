from sklearn.metrics import root_mean_squared_error
import evidently.metrics.regression_performance.regression_quality as rq


def fixed_calculate(self, data):
    # Utilisation de l'attribut _context
    rmse_score_value = root_mean_squared_error(
        y_true=data.current_data[self._context.target_name],
        y_pred=data.current_data[self._context.prediction_name],
    )
    return rmse_score_value


# Monkey patch Evidently pour utiliser root_mean_squared_error
rq.RegressionQualityMetric.calculate = fixed_calculate
