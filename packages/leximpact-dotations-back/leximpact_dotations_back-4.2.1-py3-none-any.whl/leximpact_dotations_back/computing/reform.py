import logging
from typing import Dict

from openfisca_core import periods
from openfisca_core.parameters import Parameter
from openfisca_core.reforms import Reform

from leximpact_dotations_back.mapping.reform_parameters import get_openfisca_parameter
from leximpact_dotations_back.computing.dotations_simulation import DotationsSimulation

# configure _root_ logger
logger = logging.getLogger()
REFORM_YEAR = 2024


class reform_from_amendement(Reform):
    name = 'Amendement'

    # Exemple d'amendement_parameters = {
    #     "dotation_solidarite_rurale.seuil_nombre_habitants": 5000,
    #     "dotation_solidarite_rurale.augmentation_montant": 100_000_000
    # }

    def __init__(self, baseline, amendement_parameters):
        # on définit amendement_parameters avant l'appel à super
        # à défaut on obtient cette erreur à l'exécution (du apply)
        # AttributeError: 'CountryTaxBenefitSystem' object has no attribute 'amendement_parameters'
        self.amendement_parameters: Dict[str, float] = amendement_parameters
        super().__init__(baseline)

    def reform_parameters_from_amendement(self, parameters, amendement_parameters):
        reform_period = periods.period(REFORM_YEAR)

        for parameter_name, value in amendement_parameters.items():
            try:
                one_parameter: Parameter = get_openfisca_parameter(parameters, parameter_name)
                if one_parameter is not None:
                    one_parameter.update(period=reform_period, value=value)
            except ValueError as e:
                # TODO ajouter l'information à la réponse d'API web ?
                logger.warning(f"[Amendement] Échec de la réforme du paramètre '{parameter_name}': {e}")

        return parameters

    def apply(self):
        self.modify_parameters(
            modifier_function=lambda parameters: self.reform_parameters_from_amendement(parameters, self.amendement_parameters)
        )


class reform_from_plf(Reform):
    # INFO : réforme au PLF
    # ressemble étrangement beaucoup à reform_from_amendement
    # mais cette ressemblance devrait être variable selon les années et les types de modifications apportées par chaque PLF
    name = 'PLF'

    # Exemple de plf_parameters = {
    #     "dotation_solidarite_rurale.seuil_nombre_habitants": 7000,
    #     "dotation_solidarite_rurale.augmentation_montant": 50_000_000
    # }

    def __init__(self, baseline, plf_parameters):
        # on définit plf_parameters avant l'appel à super
        # à défaut on obtient cette erreur à l'exécution (du apply)
        # AttributeError: 'CountryTaxBenefitSystem' object has no attribute 'plf_parameters'
        self.plf_parameters: Dict[str, float] = plf_parameters
        super().__init__(baseline)

    def reform_parameters_from_plf(self, parameters, plf_parameters):
        reform_period = periods.period(REFORM_YEAR)

        for parameter_name, value in plf_parameters.items():

            try:
                one_parameter: Parameter = get_openfisca_parameter(parameters, parameter_name)
                if one_parameter is not None:
                    one_parameter.update(period=reform_period, value=value)
            except ValueError as e:
                # TODO ajouter l'information à la réponse d'API web ?
                logger.warning(f"[PLF] Échec de la réforme du paramètre '{parameter_name}': {e}")

        return parameters

    def apply(self):
        self.modify_parameters(
            modifier_function=lambda parameters: self.reform_parameters_from_plf(parameters, self.plf_parameters)
        )


def get_reformed_dotations_simulation(
        reform_model,
        data_directory,
        year_period
) -> DotationsSimulation:

    dotations_simulation = DotationsSimulation(
        data_directory=data_directory,  # TODO optimiser en évitant le retraitement de criteres et adapted_criteres
        model=reform_model,
        annee=year_period
    )

    return dotations_simulation
