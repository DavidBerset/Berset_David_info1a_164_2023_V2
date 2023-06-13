"""Gestion des "routes" FLASK et des données pour les Boisson.
Fichier : gestion_boisson_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.Boisson.gestion_boisson_wtf_forms import FormWTFUpdateBoisson, FormWTFAddBoisson, FormWTFDeleteBoisson

"""Ajouter un film grâce au formulaire ".html"
Auteur : OM 2022.04.11
Définition d'une "route" /boisson_add

Test : exemple: cliquer sur le menu "Boisson/Fournisseur" puis cliquer sur le bouton "ADD" d'une "boisson"

Paramètres : sans


Remarque :  Dans le champ "nom_boisson_update_wtf" du formulaire "Boisson/boisson_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""


@app.route("/boisson_add", methods=['GET', 'POST'])
def boisson_add_wtf():
    # Objet formulaire pour AJOUTER un film
    form_add_boisson = FormWTFAddBoisson()
    if request.method == "POST":
        try:
            if form_add_boisson.validate_on_submit():
                nom_boisson_add = form_add_boisson.nom_boisson_add_wtf.data
                type_boisson_add = form_add_boisson.type_boisson_add_wtf.data
                prix_boisson_add = form_add_boisson.prix_boisson_add_wtf.data
                cover_link_boisson_add = form_add_boisson.cover_link_boisson_add_wtf.data
                code_barre_boisson_add = 54  # form_add_boisson.code_barre_boisson_add_wtf.data

                valeurs_insertion_dictionnaire = {
                                          "value_nom_boisson": nom_boisson_add,
                                          "value_type_boisson": type_boisson_add,
                                          "value_prix_vente_boisson": prix_boisson_add,
                                          "value_cover_link_boisson": cover_link_boisson_add,
                                          "value_code_barre_boisson": code_barre_boisson_add}

                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_boisson = """INSERT INTO t_boisson (nom_boisson, type_boisson, prix_vente_boisson, cover_link_boisson, code_barre_boisson)
VALUES (%(value_nom_boisson)s, %(value_type_boisson)s, %(value_prix_vente_boisson)s, %(value_cover_link_boisson)s, %(value_code_barre_boisson)s)
"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_boisson, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_boisson_sel=0 => afficher tous les Boisson)
                return redirect(url_for('boisson_fournisseur_afficher', id_boisson_sel=0))

        except Exception as Exception_fournisseur_ajouter_wtf:
            raise ExceptionFournisseurAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{boisson_add_wtf.__name__} ; "
                                            f"{Exception_fournisseur_ajouter_wtf}")

    return render_template("Boisson/boisson_add_wtf.html", form_add_boisson=form_add_boisson)


"""Editer(update) une boisson qui a été sélectionné dans le formulaire "boisson_fournisseur_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /boisson_update

Test : exemple: cliquer sur le menu "Boisson/Fournisseur" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un fournisseur qui a été sélectionné dans le formulaire "fournisseur_afficher.html"

Remarque :  Dans le champ "nom_boisson_update_wtf" du formulaire "Boisson/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/boisson_update", methods=['GET', 'POST'])
def boisson_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_fournisseur"
    id_boisson_update = request.values['id_boisson_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_boisson = FormWTFUpdateBoisson()
    try:
        print(" on submit ", form_update_boisson.validate_on_submit())
        if form_update_boisson.validate_on_submit():
            # Récupèrer la valeur du champ depuis "fournisseur_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_boisson_update = form_update_boisson.nom_boisson_update_wtf.data
            type_boisson_update = form_update_boisson.type_boisson_update_wtf.data
            prix_boisson_update = form_update_boisson.prix_boisson_update_wtf.data
            cover_link_boisson_update = form_update_boisson.cover_link_boisson_update_wtf.data
            code_barre_boisson_update = 54 #form_update_boisson.code_barre_boisson_update_wtf.data

            valeur_update_dictionnaire = {"value_id_boisson": id_boisson_update,
                                          "value_nom_boisson": nom_boisson_update,
                                          "value_type_boisson": type_boisson_update,
                                          "value_prix_vente_boisson": prix_boisson_update,
                                          "value_cover_link_boisson": cover_link_boisson_update,
                                          "value_code_barre_boisson": code_barre_boisson_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_boisson = """UPDATE t_boisson SET nom_boisson = %(value_nom_boisson)s,
                                                            type_boisson = %(value_type_boisson)s,
                                                            prix_vente_boisson = %(value_prix_vente_boisson)s,
                                                            cover_link_boisson = %(value_cover_link_boisson)s,
                                                            code_barre_boisson = %(value_code_barre_boisson)s
                                                            WHERE id_boisson = %(value_id_boisson)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_boisson, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement la boisson modifié, "ASC" et l'"id_boisson_update"
            return redirect(url_for('boisson_fournisseur_afficher', id_boisson_sel=id_boisson_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_fournisseur" et "nom_fournisseur" de la "t_fournisseur"
            str_sql_id_boisson = "SELECT * FROM t_boisson WHERE id_boisson  = %(value_id_boisson)s"
            valeur_select_dictionnaire = {"value_id_boisson": id_boisson_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_boisson, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_boisson = mybd_conn.fetchone()
            print("data_boisson ", data_boisson, " type ", type(data_boisson), " genre ",
                  data_boisson["nom_boisson"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "boisson_update_wtf.html"
            form_update_boisson.nom_boisson_update_wtf.data = data_boisson["nom_boisson"]
            form_update_boisson.type_boisson_update_wtf.data = data_boisson["type_boisson"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" type boisson  ", data_boisson["type_boisson"], "  type ", type(data_boisson["type_boisson"]))
            form_update_boisson.prix_boisson_update_wtf.data = data_boisson["prix_vente_boisson"]
            form_update_boisson.cover_link_boisson_update_wtf.data = data_boisson["cover_link_boisson"]
            form_update_boisson.code_barre_boisson_update_wtf.data = data_boisson["code_barre_boisson"]

    except Exception as Exception_boisson_update_wtf:
        raise ExceptionBoissonUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{boisson_update_wtf.__name__} ; "
                                     f"{Exception_boisson_update_wtf}")

    return render_template("Boisson/boisson_update_wtf.html", form_update_boisson=form_update_boisson)


"""Effacer(delete) une boisson qui a été sélectionné dans le formulaire "boisson_fournisseur_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /boisson_delete
    
Test : ex. cliquer sur le menu "boisson" puis cliquer sur le bouton "DELETE" d'une "boisson"
    
Paramètres : sans

Remarque :  Dans le champ "nom_boisson_delete_wtf" du formulaire "Boisson/boisson_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/boisson_delete", methods=['GET', 'POST'])
def boisson_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_boisson_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_fournisseur"
    id_boisson_delete = request.values['id_film_btn_delete_html']

    # Objet formulaire pour effacer la boisson sélectionné.
    form_delete_boisson = FormWTFDeleteBoisson()
    try:
        # Si on clique sur "ANNULER", afficher tous les Boisson.
        if form_delete_boisson.submit_btn_annuler.data:
            return redirect(url_for("boisson_fournisseur_afficher", id_boisson_sel=0))

        if form_delete_boisson.submit_btn_conf_del_boisson.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "Boisson/boisson_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_boisson_delete = session['data_boisson_delete']
            print("data_boisson_delete ", data_boisson_delete)

            flash(f"Effacer la boisson de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_boisson.submit_btn_del_boisson.data:
            valeur_delete_dictionnaire = {"value_id_boisson": id_boisson_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_pers_sortie_boisson = """
            DELETE FROM t_pers_sortie_boisson
            WHERE fk_boisson = %(value_id_boisson)s
            """

            str_sql_delete_boisson_stocker_contenance = """
            DELETE FROM t_boisson_stocker_contenance
            WHERE fk_boisson = %(value_id_boisson)s
            """

            str_sql_delete_boisson_acheter_fournisseur = """
            DELETE FROM t_boisson_acheter_fournisseur
            WHERE fk_boisson = %(value_id_boisson)s
            """

            str_sql_delete_boisson_retourner_fournisseur = """
            DELETE FROM t_boisson_retourner_fournisseur
            WHERE fk_boisson = %(value_id_boisson)s
            """

            str_sql_delete_boisson = """
            DELETE FROM t_boisson
            WHERE id_boisson = %(value_id_boisson)s
            """

            with DBconnection() as mconn_bd:
                # Supprimer les enregistrements associés dans t_pers_sortie_boisson
                mconn_bd.execute(str_sql_delete_pers_sortie_boisson, valeur_delete_dictionnaire)
                # Supprimer les enregistrements associés dans t_boisson_stocker_contenance
                mconn_bd.execute(str_sql_delete_boisson_stocker_contenance, valeur_delete_dictionnaire)
                # Supprimer les enregistrements associés dans t_boisson_acheter_fournisseur
                mconn_bd.execute(str_sql_delete_boisson_acheter_fournisseur, valeur_delete_dictionnaire)
                # Supprimer les enregistrements associés dans t_boisson_retourner_fournisseur
                mconn_bd.execute(str_sql_delete_boisson_retourner_fournisseur, valeur_delete_dictionnaire)
                # Supprimer la boisson
                mconn_bd.execute(str_sql_delete_boisson, valeur_delete_dictionnaire)

            flash(f"Boisson définitivement effacée !!", "success")
            print(f"Boisson définitivement effacée !!")

            # Afficher les données
            return redirect(url_for('boisson_fournisseur_afficher', id_boisson_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_boisson": id_boisson_delete}
            print(id_boisson_delete, type(id_boisson_delete))

            # Requête qui affiche la boisson qui doit être effacée.
            str_sql_fournisseur_boisson_delete = """
            SELECT * FROM t_fournisseur
            WHERE id_fournisseur = %(value_id_boisson)s
            """

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_fournisseur_boisson_delete, valeur_select_dictionnaire)
                data_boisson_delete = mydb_conn.fetchall()
                print("data_boisson_delete...", data_boisson_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Boisson/boisson_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_boisson_delete'] = data_boisson_delete

            # Le bouton pour l'action "DELETE" dans le form. "boisson_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_boisson_delete_wtf:
        raise ExceptionBoissonDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                        f"{boisson_delete_wtf.__name__} ; "
                                        f"{Exception_boisson_delete_wtf}")

    return render_template("Boisson/boisson_delete_wtf.html",
                            form_delete_boisson=form_delete_boisson,
                            btn_submit_del=btn_submit_del,
                            data_boisson_del=data_boisson_delete
                            )
