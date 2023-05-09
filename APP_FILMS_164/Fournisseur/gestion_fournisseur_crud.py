"""Gestion des "routes" FLASK et des données pour les Fournisseur.
Fichier : gestion_fournisseur_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.Fournisseur.gestion_fournisseur_wtf_forms import FormWTFAjouterFournisseur
from APP_FILMS_164.Fournisseur.gestion_fournisseur_wtf_forms import FormWTFDeleteFournisseur
from APP_FILMS_164.Fournisseur.gestion_fournisseur_wtf_forms import FormWTFUpdateFournisseur

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /fournisseur_afficher
    
    Test : ex : http://127.0.0.1:5575/fournisseur_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_fournisseur_sel = 0 >> tous les Fournisseur.
                id_fournisseur_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/fournisseur_afficher/<string:order_by>/<int:id_fournisseur_sel>", methods=['GET', 'POST'])
def fournisseur_afficher(order_by, id_fournisseur_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_fournisseur_sel == 0:
                    strsql_fournisseur_afficher = """SELECT t_fournisseur.id_fournisseur, t_fournisseur.nom_fournisseur, GROUP_CONCAT(DISTINCT t_mail.nom_mail) AS Email, GROUP_CONCAT(DISTINCT t_telephone.num_telephone) AS Telephone
                                                FROM t_fournisseur
                                                LEFT JOIN t_mail_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_mail_avoir_fournisseur.fk_fournisseur
                                                LEFT JOIN t_mail ON t_mail_avoir_fournisseur.fk_mail = t_mail.id_mail
                                                LEFT JOIN t_telephone_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_telephone_avoir_fournisseur.fk_fournisseur
                                                LEFT JOIN t_telephone ON t_telephone_avoir_fournisseur.fk_telephone = t_telephone.id_telephone
                                                GROUP BY t_fournisseur.id_fournisseur;
                                                """
                    mc_afficher.execute(strsql_fournisseur_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_fournisseur"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_fournisseur_selected_dictionnaire = {"value_id_genre_selected": id_fournisseur_sel}
                    strsql_fournisseur_afficher = """SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur WHERE id_fournisseur = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_fournisseur_afficher, valeur_id_fournisseur_selected_dictionnaire)
                else:
                    strsql_fournisseur_afficher = """SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur ORDER BY id_fournisseur DESC"""

                    mc_afficher.execute(strsql_fournisseur_afficher)

                data_fournisseur = mc_afficher.fetchall()

                print("data_fournisseur ", data_fournisseur, " Type : ", type(data_fournisseur))

                # Différencier les messages si la table est vide.
                if not data_fournisseur and id_fournisseur_sel == 0:
                    flash("""La table "t_fournisseur" est vide. !!""", "warning")
                elif not data_fournisseur and id_fournisseur_sel > 0:
                    # Si l'utilisateur change l'id_fournisseur dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_fournisseur" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données Fournisseur affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{fournisseur_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

        # Envoie la page "HTML" au serveur.
    return render_template("Fournisseur/fournisseur_afficher.html", data=data_fournisseur)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /fournisseur_ajouter
    
    Test : ex : http://127.0.0.1:5575/fournisseur_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour une boisson
    
    Remarque :  Dans le champ "name_fournisseur_html" du formulaire "Fournisseur/fournisseur_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/fournisseur_ajouter", methods=['GET', 'POST'])
def fournisseur_ajouter_wtf():
    form = FormWTFAjouterFournisseur()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_fournisseur = form.nom_fournisseur_wtf.data
                #name_fournisseur = name_fournisseur_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_fournisseur": name_fournisseur}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_fournisseur = """INSERT INTO t_fournisseur (id_fournisseur,nom_fournisseur) VALUES (NULL,%(value_intitule_fournisseur)s) """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_fournisseur, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('fournisseur_afficher', order_by='DESC', id_fournisseur_sel=0))

        except Exception as Exception_fournisseur_ajouter_wtf:
            raise ExceptionFournisseurAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{fournisseur_ajouter_wtf.__name__} ; "
                                            f"{Exception_fournisseur_ajouter_wtf}")

    return render_template("Fournisseur/fournisseur_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /fournisseur_update
    
    Test : ex cliquer sur le menu "Fournisseur" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "fournisseur_afficher.html"
    
    Remarque :  Dans le champ "nom_fournisseur_update_wtf" du formulaire "Fournisseur/fournisseur_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/fournisseur_update", methods=['GET', 'POST'])
def fournisseur_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_fournisseur"
    id_fournisseur_update = request.values['id_fournisseur_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateFournisseur()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "fournisseur_update_wtf.html" après avoir cliqué sur "SUBMIT".
            name_fournisseur_update = form_update.nom_fournisseur_update_wtf.data
            # Puis la convertir en lettres minuscules.
            #name_fournisseur_update = name_fournisseur_update.lower()
            date_fournisseur_essai = form_update.date_fournisseur_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_fournisseur": id_fournisseur_update,
                                          "value_name_fournisseur": name_fournisseur_update
#                                          "value_date_fournisseur_essai": date_fournisseur_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nomfournisseur = """UPDATE t_fournisseur SET nom_fournisseur = %(value_name_fournisseur)s 
            WHERE id_fournisseur = %(value_id_fournisseur)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nomfournisseur, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_fournisseur_update"
            return redirect(url_for('fournisseur_afficher', order_by="ASC", id_fournisseur_sel=id_fournisseur_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_fournisseur" et "nom_fournisseur" de la "t_fournisseur"
            str_sql_id_fournisseur = "SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur " \
                               "WHERE id_fournisseur = %(value_id_fournisseur)s"
            valeur_select_dictionnaire = {"value_id_fournisseur": id_fournisseur_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_fournisseur, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom fournisseur" pour l'UPDATE
            data_nom_fournisseur = mybd_conn.fetchone()
            print("data_nom_fournisseur ", data_nom_fournisseur, " type ", type(data_nom_fournisseur), " genre ",
                  data_nom_fournisseur["nom_fournisseur"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "fournisseur_update_wtf.html"
            form_update.nom_fournisseur_update_wtf.data = data_nom_fournisseur["nom_fournisseur"]

    except Exception as Exception_fournisseur_update_wtf:
        raise ExceptionFournisseurUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{fournisseur_update_wtf.__name__} ; "
                                      f"{Exception_fournisseur_update_wtf}")

    return render_template("Fournisseur/fournisseur_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /fournisseur_delete
    
    Test : ex. cliquer sur le menu "Fournisseur" puis cliquer sur le bouton "DELETE" d'un "fournisseur"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "fournisseur_afficher.html"
    
    Remarque :  Dans le champ "nom_fournisseur_delete_wtf" du formulaire "Fournisseur/fournisseur_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/fournisseur_delete", methods=['GET', 'POST'])
def fournisseur_delete_wtf():
    data_boisson_attribue_fournisseur_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_fournisseur"
    id_fournisseur_delete = request.values['id_fournisseur_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteFournisseur()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("fournisseur_afficher", order_by="ASC", id_fournisseur_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Fournisseur/fournisseur_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_boisson_attribue_fournisseur_delete = session['data_boisson_attribue_fournisseur_delete']
                print("data_boisson_attribue_fournisseur_delete ", data_boisson_attribue_fournisseur_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_fournisseur": id_fournisseur_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_boisson_fournisseur = """DELETE FROM t_boisson_acheter_fournisseur WHERE fk_fournisseur = %(value_id_fournisseur)s"""
                str_sql_delete_idfournisseur = """DELETE FROM t_fournisseur WHERE id_fournisseur = %(value_id_fournisseur)s"""
                # Manière brutale d'effacer d'abord la "fk_fournisseur", même si elle n'existe pas dans la "t_boisson_acheter_fournisseur"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_boisson_acheter_fournisseur"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_boisson_fournisseur, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idfournisseur, valeur_delete_dictionnaire)

                flash(f"Fournisseur définitivement effacé !!", "success")
                print(f"Fournisseur définitivement effacé !!")

                # afficher les données
                return redirect(url_for('fournisseur_afficher', order_by="ASC", id_fournisseur_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_fournisseur": id_fournisseur_delete}
            print(id_fournisseur_delete, type(id_fournisseur_delete))

            # Requête qui affiche tous les Boisson_Fournisseur qui ont le genre que l'utilisateur veut effacer
            str_sql_fournisseur_boisson_delete = """SELECT id_boisson_acheter_fournisseur, nom_boisson, id_fournisseur, nom_fournisseur FROM t_boisson_acheter_fournisseur 
                                            INNER JOIN t_boisson ON t_boisson_acheter_fournisseur.fk_boisson = t_boisson.id_boisson
                                            INNER JOIN t_fournisseur ON t_boisson_acheter_fournisseur.fk_fournisseur = t_fournisseur.id_fournisseur
                                            WHERE fk_fournisseur = %(value_id_fournisseur)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_fournisseur_boisson_delete, valeur_select_dictionnaire)
                data_boisson_attribue_fournisseur_delete = mydb_conn.fetchall()
                print("data_boisson_attribue_fournisseur_delete...", data_boisson_attribue_fournisseur_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Fournisseur/fournisseur_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_boisson_attribue_fournisseur_delete'] = data_boisson_attribue_fournisseur_delete

                # Opération sur la BD pour récupérer "id_fournisseur" et "nom_fournisseur" de la "t_fournisseur"
                str_sql_id_fournisseur = "SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur WHERE id_fournisseur = %(value_id_fournisseur)s"

                mydb_conn.execute(str_sql_id_fournisseur, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_fournisseur = mydb_conn.fetchone()
                print("data_nom_fournisseur ", data_nom_fournisseur, " type ", type(data_nom_fournisseur), " fournisseur ",
                      data_nom_fournisseur["nom_fournisseur"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "fournisseur_delete_wtf.html"
            form_delete.nom_fournisseur_delete_wtf.data = data_nom_fournisseur["nom_fournisseur"]

            # Le bouton pour l'action "DELETE" dans le form. "fournisseur_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_fournisseur_delete_wtf:
        raise ExceptionFournisseurDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{fournisseur_delete_wtf.__name__} ; "
                                      f"{Exception_fournisseur_delete_wtf}")

    return render_template("Fournisseur/fournisseur_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_boisson_associes=data_boisson_attribue_fournisseur_delete)