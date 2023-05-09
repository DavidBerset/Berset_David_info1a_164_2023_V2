"""
    Fichier : gestion_fournisseur_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterFournisseur(FlaskForm):
    """
        Dans le formulaire "fournisseur_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_fournisseur_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_fournisseur_wtf = StringField("Insérer le fournisseurs", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_fournisseur_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    submit = SubmitField("Enregistrer le fournisseur")


class FormWTFUpdateFournisseur(FlaskForm):
    """
        Dans le formulaire "fournisseur_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
        Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
    """
    nom_fournisseur_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_fournisseur_update_wtf = StringField("Clavioter le fournisseur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_fournisseur_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_fournisseur_wtf_essai = StringField("Clavioter le fournisseur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_fournisseur_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    #date_fournisseur_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
    #                                                           DataRequired("Date non valide")])
    submit = SubmitField("Update le fournisseur")


class FormWTFDeleteFournisseur(FlaskForm):
    """
        Dans le formulaire "fournisseur_delete_wtf.html"

        nom_fournisseur_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_fournisseur".
    """
    nom_fournisseur_delete_wtf = StringField("Effacer ce fournisseur")
    submit_btn_del = SubmitField("Effacer fournisseur")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")