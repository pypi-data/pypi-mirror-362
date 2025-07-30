#include <nuTens/propagator/propagator.hpp>

Tensor Propagator::calculateProbs()
{
    NT_PROFILE();

    Tensor ret;

    // if a matter solver was specified, use effective values for masses and PMNS
    // matrix, otherwise just use the "raw" ones
    if (_matterSolver != nullptr)
    {
        Tensor eigenVals =
            Tensor::zeros({1, _nGenerations, _nGenerations}, NTdtypes::kComplexFloat).requiresGrad(false);
        Tensor eigenVecs =
            Tensor::zeros({1, _nGenerations, _nGenerations}, NTdtypes::kComplexFloat).requiresGrad(false);

        _matterSolver->calculateEigenvalues(eigenVecs, eigenVals);
        Tensor effectiveMassesSq = Tensor::mul(eigenVals, Tensor::scale(_energies, 2.0));
        Tensor effectivePMNS = Tensor::matmul(_pmnsMatrix, eigenVecs);

        ret = _calculateProbs(effectiveMassesSq, effectivePMNS);
    }

    else
    {
        ret = _calculateProbs(Tensor::mul(_masses, _masses), _pmnsMatrix);
    }

    return ret;
}

Tensor Propagator::_calculateProbs(const Tensor &massesSq, const Tensor &PMNS)
{
    NT_PROFILE();

    Tensor weightVector = Tensor::exp(
        Tensor::div(massesSq, _weightArgDenom));

    _weightMatrix.requiresGrad(false);
    for (int i = 0; i < _nGenerations; i++)
    {
        for (int j = 0; j < _nGenerations; j++)
        {
            _weightMatrix.setValue({"...", i, j}, weightVector.getValues({"...", j}));
        }
    }
    _weightMatrix.requiresGrad(true);

    Tensor sqrtProbabilities = Tensor::matmul(PMNS.conj(), Tensor::transpose(Tensor::mul(PMNS, _weightMatrix), 1, 2));

    return Tensor::pow(sqrtProbabilities.abs(), 2);
}
