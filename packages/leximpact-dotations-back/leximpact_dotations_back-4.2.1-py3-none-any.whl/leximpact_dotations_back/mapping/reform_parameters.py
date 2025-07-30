import logging
from openfisca_core.parameters import Parameter, ParameterNode


# configure _root_ logger
logger = logging.getLogger()


def extract_openfisca_parameter(parameters: ParameterNode, parameter_dot_name: str) -> Parameter | None:
    '''
    Extrait le Parameter openfisca de l'arbre des paramètres fourni
    à partir de son nom en notation pointée.
    '''
    parameter_name: str = parameter_dot_name

    is_scale_bracket: bool = False
    bracket_openfisca_index: int | None = None
    remaining_path: str | None = None

    if 'brackets' in parameter_dot_name:
        is_scale_bracket = True

        start_bracket_index = parameter_dot_name.index('.brackets[') + 10  # 10 pour longueur '.brackets['
        parameter_name = parameter_dot_name[:start_bracket_index - 10]  # tout ce qui précède '.brackets['

        end_bracket_index = parameter_dot_name.index(']')
        bracket_openfisca_index = int(parameter_dot_name[start_bracket_index:end_bracket_index])

        # le remaining_path attendu est 'threshold', 'rate' ou 'amount'
        remaining_path = parameter_dot_name[end_bracket_index + 2:]  # 2 pour longueur "]."

    try:
        # pour un paramètre simple, parameter_name est le nom fourni en argument
        # pour un barème, parameter_name est le nom fourni en argument tronqué à partir de '.brackets'
        cles = parameter_name.split('.')

        for cle in cles:
            parameters = parameters.children[cle]

        if is_scale_bracket:
            # parameters.brackets est list[ParameterScaleBracket]
            # mais structure étrange : parameters.brackets[bracket_openfisca_index] est un ParameterNode
            parameters = parameters.brackets[bracket_openfisca_index].children[remaining_path]

        logger.debug(f"La valeur correspondante à '{parameter_name}' est : {parameters}")
        return parameters  # un Parameter si parameter_dot_name indique bien une feuille de l'arbre des parameters

    except KeyError:
        # La clé '{cle}' n'a pas été trouvée dans modèle
        logger.error(f"Paramètre '{parameter_name}' introuvable.")
        return None
    except AttributeError:
        logger.error(f"La structure de l'arbre de paramètres n'est pas un dictionnaire à partir de : {parameters}")
        return None


def get_openfisca_parameter(openfisca_parameters: ParameterNode, openfisca_parameter_suffix: str) -> Parameter:
    identified_reform_parameters_2024 = {
        # DF
        # "dotation_forfaitaire.montant_minimum_par_habitant",
        # "dotation_forfaitaire.montant_maximum_par_habitant",
        "dotation_forfaitaire.ecretement.plafond_pourcentage_recettes_max": openfisca_parameters.dotation_forfaitaire.ecretement.plafond_pourcentage_recettes_max,
        "dotation_forfaitaire.ecretement.seuil_rapport_potentiel_fiscal": openfisca_parameters.dotation_forfaitaire.ecretement.seuil_rapport_potentiel_fiscal,

        # DSR
        "dotation_solidarite_rurale.attribution.plafond_effort_fiscal": openfisca_parameters.dotation_solidarite_rurale.attribution.plafond_effort_fiscal,
        "dotation_solidarite_rurale.attribution.poids_enfants": openfisca_parameters.dotation_solidarite_rurale.attribution.poids_enfants,
        "dotation_solidarite_rurale.attribution.poids_longueur_voirie": openfisca_parameters.dotation_solidarite_rurale.attribution.poids_longueur_voirie,
        "dotation_solidarite_rurale.attribution.poids_potentiel_financier_par_habitant": openfisca_parameters.dotation_solidarite_rurale.attribution.poids_potentiel_financier_par_habitant,
        "dotation_solidarite_rurale.attribution.poids_potentiel_financier_par_hectare": openfisca_parameters.dotation_solidarite_rurale.attribution.poids_potentiel_financier_par_hectare,
        "dotation_solidarite_rurale.augmentation_montant": openfisca_parameters.dotation_solidarite_rurale.augmentation_montant,
        "dotation_solidarite_rurale.bourg_centre.attribution.coefficient_zrr": openfisca_parameters.dotation_solidarite_rurale.bourg_centre.attribution.coefficient_zrr,
        "dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_part_population_dgf_agglomeration_departement": openfisca_parameters.dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_part_population_dgf_agglomeration_departement,
        "dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_population_dgf_agglomeration": openfisca_parameters.dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_population_dgf_agglomeration,
        "dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_population_dgf_chef_lieu_de_canton": openfisca_parameters.dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_population_dgf_chef_lieu_de_canton,
        "dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_population_dgf_maximum_commune_agglomeration": openfisca_parameters.dotation_solidarite_rurale.bourg_centre.eligibilite.exclusion.seuil_population_dgf_maximum_commune_agglomeration,
        "dotation_solidarite_rurale.bourg_centre.eligibilite.seuil_nombre_habitants_chef_lieu": openfisca_parameters.dotation_solidarite_rurale.bourg_centre.eligibilite.seuil_nombre_habitants_chef_lieu,
        "dotation_solidarite_rurale.bourg_centre.eligibilite.seuil_part_population_canton": openfisca_parameters.dotation_solidarite_rurale.bourg_centre.eligibilite.seuil_part_population_canton,
        "dotation_solidarite_rurale.cible.eligibilite.indice_synthetique.poids_potentiel_financier": openfisca_parameters.dotation_solidarite_rurale.cible.eligibilite.indice_synthetique.poids_potentiel_financier,
        "dotation_solidarite_rurale.cible.eligibilite.indice_synthetique.poids_revenu": openfisca_parameters.dotation_solidarite_rurale.cible.eligibilite.indice_synthetique.poids_revenu,
        "dotation_solidarite_rurale.cible.eligibilite.seuil_classement": openfisca_parameters.dotation_solidarite_rurale.cible.eligibilite.seuil_classement,
        "dotation_solidarite_rurale.perequation.seuil_rapport_potentiel_financier": openfisca_parameters.dotation_solidarite_rurale.perequation.seuil_rapport_potentiel_financier,
        "dotation_solidarite_rurale.seuil_nombre_habitants": openfisca_parameters.dotation_solidarite_rurale.seuil_nombre_habitants,

        # DSU
        "dotation_solidarite_urbaine.attribution.facteur_classement_max": openfisca_parameters.dotation_solidarite_urbaine.attribution.facteur_classement_max,
        "dotation_solidarite_urbaine.attribution.facteur_classement_min": openfisca_parameters.dotation_solidarite_urbaine.attribution.facteur_classement_min,
        "dotation_solidarite_urbaine.attribution.plafond_effort_fiscal": openfisca_parameters.dotation_solidarite_urbaine.attribution.plafond_effort_fiscal,
        "dotation_solidarite_urbaine.attribution.poids_quartiers_prioritaires_ville": openfisca_parameters.dotation_solidarite_urbaine.attribution.poids_quartiers_prioritaires_ville,
        "dotation_solidarite_urbaine.attribution.poids_zone_franche_urbaine": openfisca_parameters.dotation_solidarite_urbaine.attribution.poids_zone_franche_urbaine,
        "dotation_solidarite_urbaine.augmentation_montant": openfisca_parameters.dotation_solidarite_urbaine.augmentation_montant,
        "dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_aides_au_logement": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_aides_au_logement,
        "dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_logements_sociaux": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_logements_sociaux,
        "dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_potentiel_financier": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_potentiel_financier,
        "dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_revenu": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.indice_synthetique.poids_revenu,
        "dotation_solidarite_urbaine.eligibilite.part_eligible_seuil_bas": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.part_eligible_seuil_bas,
        "dotation_solidarite_urbaine.eligibilite.part_eligible_seuil_haut": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.part_eligible_seuil_haut,
        "dotation_solidarite_urbaine.eligibilite.seuil_bas_nombre_habitants": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.seuil_bas_nombre_habitants,
        "dotation_solidarite_urbaine.eligibilite.seuil_haut_nombre_habitants": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.seuil_haut_nombre_habitants,
        "dotation_solidarite_urbaine.eligibilite.seuil_rapport_potentiel_financier": openfisca_parameters.dotation_solidarite_urbaine.eligibilite.seuil_rapport_potentiel_financier,

        # Critères généraux
        "population.plafond_dgf.brackets[0].amount": openfisca_parameters.population.plafond_dgf.brackets[0].amount,
        "population.plafond_dgf.brackets[1].amount": openfisca_parameters.population.plafond_dgf.brackets[1].amount,
        "population.plafond_dgf.brackets[2].amount": openfisca_parameters.population.plafond_dgf.brackets[2].amount,
        "population.plafond_dgf.brackets[1].threshold": openfisca_parameters.population.plafond_dgf.brackets[1].threshold,
        "population.plafond_dgf.brackets[3].threshold": openfisca_parameters.population.plafond_dgf.brackets[3].threshold
    }

    parameter: Parameter | None = identified_reform_parameters_2024.get(openfisca_parameter_suffix)
    if parameter is None:
        parameter = extract_openfisca_parameter(
            openfisca_parameters,
            openfisca_parameter_suffix
        )

    return parameter
