
#include "Transformation.h"
/* 
 Sinh-arcsinh distribution from Jones and Pewsey (2009, p.2)
 Note that initial implementation of Sinh-arcsinh transformation (SinhAsinhTransformation.cpp) assumes that
 transformed data follows a normal dist with a specified mean and standard deviation.
 This implementation assumes that transformed zscore (transformation after rescaling data with shift = -mean and scale = 1/stdDev) follows a standard normal dist
 References:
 1. Jones, M. C., & Pewsey, A. (2009). Sinh-arcsinh distributions. Biometrika, 96(4), 761-780. doi:10.1093/biomet/asp053
 2. https://rpubs.com/FJRubio/SAS
 3. https://search.r-project.org/CRAN/refmans/gamlss.dist/html/SHASH.html
*/

using namespace std;


JonesPewseyTransformation::JonesPewseyTransformation()
{
    m_transDelta = 0.0;
    m_transEpsilon = 1.0;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



JonesPewseyTransformation::JonesPewseyTransformation(double transDelta, double transEpsilon)
{
    m_transDelta = transDelta;
    m_transEpsilon = transEpsilon;
    m_scale = 1.0;
    m_shift = 0.0;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}



JonesPewseyTransformation::JonesPewseyTransformation(double transDelta, double transEpsilon, double scale, double shift)
{
    m_transDelta = transDelta;
    m_transEpsilon = transEpsilon;
    m_scale = scale;
    m_shift = shift;
    m_transMean = -9999.;
    m_transStdDev = -9999.;
}


double JonesPewseyTransformation::transformOne(double value)
{
	return transformOne(value, m_transDelta, m_transEpsilon);
}



double JonesPewseyTransformation::transformOne(double value, double transDelta, double transEpsilon)
{

	return sinh(transDelta * asinh(value) + transEpsilon);
}



double JonesPewseyTransformation::invTransformOne(double value)
{
	return invTransformOne(value, m_transDelta, m_transEpsilon);
}



double JonesPewseyTransformation::invTransformOne(double value, double transDelta, double transEpsilon)
{

	double transValue = sinh((asinh(value) - transEpsilon) / transDelta);

	return transValue;
}


double JonesPewseyTransformation::logDensityTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transDelta = params[0];
    double transEpsilon = params[1];

    double logDens;
	double zscore;
	double transZscore;

    if (transData > leftCensThresh && transData < rightCensThresh) {
		
        zscore = (data - mean) / stdDev;
		transZscore = transformOne(zscore, transDelta, transEpsilon);
		
		//logDens = normLogPdf(transData, mean, stdDev);
		logDens = normLogPdf(transZscore, 0.0, 1.0);
        // Jacobian
        //logDens += log(transDelta * cosh(transDelta * asinh(data) + transEpsilon) / sqrt(pow(data,2) + 1));
		logDens += log(transDelta) + log(cosh(transDelta * asinh(zscore) + transEpsilon)) - 0.5 * log(1 + pow(zscore,2)) - log(stdDev);

    } else if (transData <= leftCensThresh) {

        logDens = log(stdNormCdf((leftCensThresh-mean)/stdDev) );

    } else {

        logDens = log(1 - stdNormCdf((rightCensThresh-mean)/stdDev) );

    }

    return logDens;

}

double JonesPewseyTransformation::logJacobianTransformed(vector<double>& params, double transData, double data, double leftCensThresh, double rightCensThresh)
{

    double mean = params[2];
    double stdDev = params[3];
    double transDelta = params[0];
    double transEpsilon = params[1];

    double logJac;
	double zscore;
	double transZscore;

    if (transData > leftCensThresh && transData < rightCensThresh) {

        //logJac = log( transDelta * cosh(transDelta * asinh(data) + transEpsilon) * 1/sqrt(pow(data,2) + 1));
		zscore = (data - mean) / stdDev;
		transZscore = transformOne(zscore, transDelta, transEpsilon);
		logJac = log(transDelta) + log(cosh(transDelta * asinh(zscore) + transEpsilon)) - 0.5 * log(1 + pow(zscore,2)) - log(stdDev);

    } else if (transData <= leftCensThresh) {

        logJac = 0.0;

    } else {

        logJac = 0.0;

    }

    return logJac;

}



vector<double> JonesPewseyTransformation::convertParams(vector<double>& params)
{

    // Delta, epsilon, mean, stdev

    double delta = params[0] / (1 - params[0]);
    vector<double> newParams = {delta,
                                params[1] / sqrt(1 - pow(params[1],2)),
                                params[2] / sqrt(1 - pow(params[2],2)),
                                delta * params[3] / (1 - params[3])};

    // set transformation parameter fields
    m_transDelta = newParams[0];
    m_transEpsilon = newParams[1];
    m_transMean = newParams[2];
    m_transStdDev = newParams[3];

    return newParams;
}



double JonesPewseyTransformation::priorDensity() {

    double reparam_delta = m_transDelta / (1 + m_transDelta);
    double reparam_epsilon = m_transEpsilon / sqrt(1 + m_transEpsilon * m_transEpsilon);

    return (normLogPdf(reparam_delta, getPriorMean(), getPriorStdDev()) + normLogPdf(reparam_epsilon, 0.0,1.0));
}


vector<double> JonesPewseyTransformation::getScaleShift() {

    vector<double> params = {m_scale, m_shift};

    return params;
}


vector<double> JonesPewseyTransformation::getTransformationParams () {

    vector<double> params = {m_transDelta, m_transEpsilon};

    return params;
}

vector<double> JonesPewseyTransformation::getDistributionParams () {

    vector<double> params = {m_transDelta, m_transEpsilon, m_transMean, m_transStdDev};

    return params;

}