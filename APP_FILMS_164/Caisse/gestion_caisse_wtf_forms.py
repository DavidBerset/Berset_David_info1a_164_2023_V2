"""
    Fichier : gestion_caisse_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterCaisse(FlaskForm):
    """
        Dans le formulaire "caisse_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    # date_Caisse_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    # date_Caisse_wtf = StringField("Insérer le fournisseurs", validators=[Length(min=2, max=20, message="min 2 max 20"),
    #                                                                Regexp(date_caisse_regexp,
    #                                                                       message="Pas de chiffres, de caractères "
    #                                                                               "spéciaux, "
    #                                                                               "d'espace à double, de double "
    #                                                                               "apostrophe, de double trait union")
    #                                                                ])
    submit = SubmitField("Enregistrer la nouvelle date de caisse")


class FormWTFUpdateCaisse(FlaskForm):
    """
        Dans le formulaire "caisse_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
        Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
    """
    # date_caisse_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    # date_caisse_update_wtf = StringField("Clavioter la date de la caisse ", validators=[Length(min=2, max=20, message="min 2 max 20"),
    #                                                                       Regexp(date_caisse_update_regexp,
    #                                                                              message="Pas de chiffres, de "
    #                                                                                      "caractères "
    #                                                                                      "spéciaux, "
    #                                                                                      "d'espace à double, de double "
    #                                                                                      "apostrophe, de double trait "
    #                                                                                      "union")
    #                                                                       ])
    caisse_avant_fete_wtf_essai = StringField("Clavioter le montant dans la caisse avant la fête ")#, validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          # Regexp(nom_fournisseur_update_regexp,
                                                                          #        message="Pas de chiffres, de "
                                                                          #                "caractères "
                                                                          #                "spéciaux, "
                                                                          #                "d'espace à double, de double "
                                                                          #                "apostrophe, de double trait "
                                                                          #                "union")
                                                                          # ])

    submit = SubmitField("Update la caisse")


class FormWTFDeleteCaisse(FlaskForm):
    """
        Dans le formulaire "caisse_delete_wtf.html"

        date_caisse_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_fournisseur".
    """
    date_caisse_delete_wtf = StringField("Effacer cette date de caisse")
    submit_btn_del = SubmitField("Effacer caisse")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
