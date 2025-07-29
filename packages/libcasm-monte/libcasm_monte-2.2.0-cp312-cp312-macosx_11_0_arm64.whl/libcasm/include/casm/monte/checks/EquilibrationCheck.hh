#ifndef CASM_monte_EquilibrationCheck
#define CASM_monte_EquilibrationCheck

#include "casm/monte/checks/ConvergenceCheck.hh"
#include "casm/monte/definitions.hh"
#include "casm/monte/sampling/Sampler.hh"

namespace CASM {
namespace monte {

/// \brief Equilibration check result data structure (individual component)
struct IndividualEquilibrationCheckResult {
  /// \brief True if equilibration check performed and value is equilibrated
  ///
  /// \seealso `equilibration_check` for calculation details
  bool is_equilibrated = false;

  /// \brief Number of samples involved in equilibration (for this value only)
  ///
  /// Notes:
  /// - Multiple values may be requested for equilibration and convergence, so
  /// statistics are only taken when *all* requested values are equilibrated.
  CountType N_samples_for_equilibration = 0;
};

/// \brief Check if a range of observations have equilibrated
IndividualEquilibrationCheckResult default_equilibration_check(
    Eigen::VectorXd const &observations, Eigen::VectorXd const &sample_weight,
    RequestedPrecision requested_precision);

/// \brief Equilibration check results data structure (all requested components)
struct EquilibrationCheckResults {
  /// \brief True if all required properties are equilibrated to the requested
  /// precision
  ///
  /// Notes:
  /// - True if completion check finds all required properties are equilibrated
  /// to the requested precision
  /// - False otherwise, including if no convergence checks were requested
  bool all_equilibrated = false;

  /// How long (how many samples) it took for all requested values to
  /// equilibrate; set to 0 if no convergence checks were requested
  CountType N_samples_for_all_to_equilibrate = 0;

  /// Results from checking equilibration criteria
  std::map<SamplerComponent, IndividualEquilibrationCheckResult>
      individual_results;
};

EquilibrationCheckResults equilibration_check(
    EquilibrationCheckFunction equilibration_check_f,
    std::map<SamplerComponent, RequestedPrecision> const &requested_precision,
    std::map<std::string, std::shared_ptr<Sampler>> const &samplers,
    Sampler const &sample_weight, bool check_all);

}  // namespace monte
}  // namespace CASM

#endif
