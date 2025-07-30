from .marginalized_extrinsic import MarginalizedExtrinsicLikelihood


class MarginalizedExtrinsicLikelihoodLensingTypeII(
        MarginalizedExtrinsicLikelihood):
    """Assume GW is a type II image."""
    def _get_dh_hh_timeshift(self, par_dic):
        dh_mptd, hh_mppd, timeshift = super()._get_dh_hh_timeshift(par_dic)
        return -1j * dh_mptd, hh_mppd, timeshift
