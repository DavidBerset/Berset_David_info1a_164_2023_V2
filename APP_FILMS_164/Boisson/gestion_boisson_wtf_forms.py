"""Gestion des formulaires avec WTF pour les Boisson
Fichier : gestion_boisson_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddBoisson(FlaskForm):
    """
        Dans le formulaire "fournisseur_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_boisson_regexp = ""
    nom_boisson_add_wtf = StringField("Nom de la boisson", validators=[Length(min=2, max=2000, message="min 2 max 20"),
                                                               Regexp(nom_boisson_regexp,
                                                                      message="Pas de chiffres, de caractères "
                                                                              "spéciaux, "
                                                                              "d'espace à double, de double "
                                                                              "apostrophe, de double trait union")
                                                               ])

    submit = SubmitField("Enregistrer boisson")


class FormWTFDeleteBoisson(FlaskForm):
    """
        Dans le formulaire "boisson_delete_wtf.html"

        nom_boisson_delete_wtf : Champ qui reçoit la valeur de la boisson, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer une "boisson".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_fournisseur".
    """
    nom_boisson_delete_wtf = StringField("Effacer cette boisson")
    submit_btn_del_boisson = SubmitField("Effacer boisson")
    submit_btn_conf_del_boisson = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
