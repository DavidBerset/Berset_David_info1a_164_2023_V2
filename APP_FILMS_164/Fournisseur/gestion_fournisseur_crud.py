"""Gestion des "routes" FLASK et des données pour les Fournisseur.
Fichier : gestion_fournisseur_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path
import re
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.Fournisseur.gestion_fournisseur_wtf_forms import FormWTFAjouterFournisseur, FormWTFTelephone, FormWTFDeleteFournisseur, FormWTFUpdateFournisseur

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
                    strsql_fournisseur_afficher = """SELECT t_fournisseur.id_fournisseur, t_fournisseur.nom_fournisseur, GROUP_CONCAT(DISTINCT t_mail.nom_mail) AS Email, GROUP_CONCAT(DISTINCT t_telephone.num_telephone) AS Telephone, GROUP_CONCAT(DISTINCT CONCAT_WS(', ', t_adresse.nom_rue_adresse, t_adresse.ville_adresse, t_adresse.npa_adresse)) AS Adresse
                                                    FROM t_fournisseur
                                                    LEFT JOIN t_mail_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_mail_avoir_fournisseur.fk_fournisseur
                                                    LEFT JOIN t_mail ON t_mail_avoir_fournisseur.fk_mail = t_mail.id_mail
                                                    LEFT JOIN t_telephone_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_telephone_avoir_fournisseur.fk_fournisseur
                                                    LEFT JOIN t_telephone ON t_telephone_avoir_fournisseur.fk_telephone = t_telephone.id_telephone
                                                    LEFT JOIN t_adresse_etre_fournisseur ON t_fournisseur.id_fournisseur = t_adresse_etre_fournisseur.fk_fournisseur
                                                    LEFT JOIN t_adresse ON t_adresse_etre_fournisseur.fk_adresse = t_adresse.id_adresse
                                                    GROUP BY t_fournisseur.id_fournisseur;
                                                    """
                    mc_afficher.execute(strsql_fournisseur_afficher)
                elif order_by == "ASC":
                    # C'EST ICI QUE VOUS DEVEZ METTRE VOTRE LOGIQUE MySql PERSONNALISÉE
                    # La commande MySql classique est "SELECT * FROM t_fournisseur"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table,
                    # je précise les champs à afficher.
                    # Constitution d'un dictionnaire pour associer l'id du fournisseur sélectionné avec un nom de variable
                    valeur_id_fournisseur_selected_dictionnaire = {"value_id_fournisseur_selected": id_fournisseur_sel}
                    strsql_fournisseur_afficher = """SELECT t_fournisseur.id_fournisseur, t_fournisseur.nom_fournisseur, GROUP_CONCAT(DISTINCT t_mail.nom_mail) AS Email, GROUP_CONCAT(DISTINCT t_telephone.num_telephone) AS Telephone, GROUP_CONCAT(DISTINCT CONCAT_WS(', ', t_adresse.nom_rue_adresse, t_adresse.ville_adresse, t_adresse.npa_adresse)) AS Adresse
                                                        FROM t_fournisseur
                                                        LEFT JOIN t_mail_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_mail_avoir_fournisseur.fk_fournisseur
                                                        LEFT JOIN t_mail ON t_mail_avoir_fournisseur.fk_mail = t_mail.id_mail
                                                        LEFT JOIN t_telephone_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_telephone_avoir_fournisseur.fk_fournisseur
                                                        LEFT JOIN t_telephone ON t_telephone_avoir_fournisseur.fk_telephone = t_telephone.id_telephone
                                                        LEFT JOIN t_adresse_etre_fournisseur ON t_fournisseur.id_fournisseur = t_adresse_etre_fournisseur.fk_fournisseur
                                                        LEFT JOIN t_adresse ON t_adresse_etre_fournisseur.fk_adresse = t_adresse.id_adresse
                                                        WHERE t_fournisseur.id_fournisseur = %(value_id_fournisseur_selected)s
                                                        GROUP BY t_fournisseur.id_fournisseur;
                                                    """

                    mc_afficher.execute(strsql_fournisseur_afficher, valeur_id_fournisseur_selected_dictionnaire)
                else:
                    strsql_fournisseur_afficher = """SELECT t_fournisseur.id_fournisseur, t_fournisseur.nom_fournisseur, GROUP_CONCAT(DISTINCT t_mail.nom_mail) AS Email, GROUP_CONCAT(DISTINCT t_telephone.num_telephone) AS Telephone, GROUP_CONCAT(DISTINCT CONCAT_WS(', ', t_adresse.nom_rue_adresse, t_adresse.ville_adresse, t_adresse.npa_adresse)) AS Adresse
                                                    FROM t_fournisseur
                                                    LEFT JOIN t_mail_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_mail_avoir_fournisseur.fk_fournisseur
                                                    LEFT JOIN t_mail ON t_mail_avoir_fournisseur.fk_mail = t_mail.id_mail
                                                    LEFT JOIN t_telephone_avoir_fournisseur ON t_fournisseur.id_fournisseur = t_telephone_avoir_fournisseur.fk_fournisseur
                                                    LEFT JOIN t_telephone ON t_telephone_avoir_fournisseur.fk_telephone = t_telephone.id_telephone
                                                    LEFT JOIN t_adresse_etre_fournisseur ON t_fournisseur.id_fournisseur = t_adresse_etre_fournisseur.fk_fournisseur
                                                    LEFT JOIN t_adresse ON t_adresse_etre_fournisseur.fk_adresse = t_adresse.id_adresse
                                                    GROUP BY t_fournisseur.id_fournisseur
                                                    ORDER BY t_fournisseur.id_fournisseur DESC;
                                                    """

                    mc_afficher.execute(strsql_fournisseur_afficher)

                data_fournisseur = mc_afficher.fetchall()

                print("data_fournisseur ", data_fournisseur, " Type : ", type(data_fournisseur))

                # Différencier les messages si la table est vide.
                if not data_fournisseur and id_fournisseur_sel == 0:
                    flash("""La table "t_fournisseur" est vide. !!""", "warning")
                elif not data_fournisseur and id_fournisseur_sel > 0:
                    # Si l'utilisateur change l'id_fournisseur dans l'URL et que le fournisseur n'existe pas,
                    flash(f"Le fournisseur demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, les données des fournisseurs sont affichées.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner une indication rassurante aux utilisateurs.
                    flash(f"Données fournisseurs affichées !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{fournisseur_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Fournisseur/fournisseur_afficher.html", data=data_fournisseur)

"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /fournisseur_ajouter
    
    Test : ex : http://127.0.0.1:5575/caisse_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour une boisson
    
    Remarque :  Dans le champ "name_fournisseur_html" du formulaire "Fournisseur/caisse_ajouter.html",
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
        # On récupère la liste des champs de téléphone
        KeyListTelephone = list(filter(re.compile("^telephone\d+$").match, request.values.keys()))
        # On remet les téléphone dans le sous-formulaire
        telephones = []
        for keytel in KeyListTelephone:
            tel_form = FormWTFTelephone()
            tel_form.telephone.id = int(keytel.replace("telephone", ""))
            tel_form.telephone.name = keytel
            tel_form.telephone.data = request.values[keytel]
            telephones.append(tel_form)
        form_update.telephones = telephones

        if form_update.ajoute_tel.data:
            tel_form = FormWTFTelephone()
            tel_form.telephone.name = "telephone0"
            form_update.telephones.append(tel_form)

        elif form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "fournisseur_update_wtf.html" après avoir cliqué sur "SUBMIT".
            name_fournisseur_update = form_update.nom_fournisseur_update_wtf.data
            email_fournisseur_essai = form_update.email_fournisseur_wtf_essai.data
            telephone_fournisseur_essai = form_update.telephone_fournisseur_wtf_essai.data

            valeur_update_dictionnaire = {
                "value_id_fournisseur": id_fournisseur_update,
                "value_name_fournisseur": name_fournisseur_update,
                "email_fournisseur": email_fournisseur_essai,
                "telephone_fournisseur": telephone_fournisseur_essai,
                "nom_rue_adresse": form_update.nom_rue_adresse.data,
                "ville_fournisseur": form_update.ville_fournisseur.data,
                "code_postal_fournisseur": form_update.code_postal_fournisseur.data
            }

            # boucler sur la liste des numéro
            #   et mise a jours des numéros avec un id supérieur et égal a 1
            #   puis exectuer pour chacun des autre un ajout en db
            for telephoneForm in form_update.telephones:
                str_sql_action_telephone =""
                print(telephoneForm.telephone.id)
                if telephoneForm.telephone.id >= 1:
                    valeur_update_dictionnaire["id_telephone"] = telephoneForm.telephone.id
                    valeur_update_dictionnaire["numero_telephone"] = telephoneForm.telephone.data
                    str_sql_action_telephone = """
                    UPDATE t_telephone AS tel
                    SET tel.num_telephone = %(numero_telephone)s
                    WHERE tel.id_telephone = %(id_telephone)s
                    """
                    with DBconnection() as mconn_bd:
                        mconn_bd.execute(str_sql_action_telephone, valeur_update_dictionnaire)
                else:
                    # création du numéro de telephone
                    valeur_update_dictionnaire["numero_telephone"] = telephoneForm.telephone.data
                    str_sql_action_telephone = """
                    INSERT INTO t_telephone (id_telephone,num_telephone) VALUES (NULL,%(numero_telephone)s)
                    """
                    with DBconnection() as mconn_bd:
                        mconn_bd.execute(str_sql_action_telephone, valeur_update_dictionnaire)

                    # ajout de la jointure avec le fournisseur
                    valeur_update_dictionnaire["id_telephone"] = mconn_bd.lastrowid
                    str_sql_action_telephone = """
                    INSERT INTO t_telephone_avoir_fournisseur (fk_telephone,fk_fournisseur) 
                    VALUES (%(id_telephone)s,%(value_id_fournisseur)s)
                    """
                    with DBconnection() as mconn_bd:
                        mconn_bd.execute(str_sql_action_telephone, valeur_update_dictionnaire)


            # str_sql_update_telephone = """
            # UPDATE t_telephone AS tel
            # JOIN t_telephone_avoir_fournisseur AS t ON t.fk_telephone = tel.id_telephone
            # JOIN t_fournisseur AS f ON t.fk_fournisseur = f.id_fournisseur
            # SET tel.num_telephone = %(telephone_fournisseur)s
            # WHERE f.id_fournisseur = %(value_id_fournisseur)s
            # AND NOT EXISTS (
            #     SELECT * FROM t_telephone_avoir_fournisseur AS t2
            #     WHERE t2.fk_telephone = tel.id_telephone
            #     AND t2.fk_fournisseur != %(value_id_fournisseur)s
            # )
            # """

            str_sql_update_email = """
            UPDATE t_mail AS mail
            JOIN t_mail_avoir_fournisseur AS m ON m.fk_mail = mail.id_mail
            JOIN t_fournisseur AS f ON m.fk_fournisseur = f.id_fournisseur
            JOIN t_adresse_etre_fournisseur AS af ON af.fk_fournisseur = f.id_fournisseur
            JOIN t_adresse AS a ON af.fk_adresse = a.id_adresse
            SET mail.nom_mail = %(email_fournisseur)s,
                a.nom_rue_adresse = %(nom_rue_adresse)s,
                a.ville_adresse = %(ville_fournisseur)s,
                a.npa_adresse = %(code_postal_fournisseur)s
            WHERE f.id_fournisseur = %(value_id_fournisseur)s
            """

            # Exécution des requêtes SQL
            with DBconnection() as mconn_bd:
               # mconn_bd.execute(str_sql_update_telephone, valeur_update_dictionnaire)
                mconn_bd.execute(str_sql_update_email, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")

            # Redirection vers la page d'affichage des fournisseurs
            return redirect(url_for('fournisseur_afficher', order_by="ASC", id_fournisseur_sel=id_fournisseur_update))

        elif request.method == "GET":
            # Opération sur la BD pour récupérer les informations du fournisseur à mettre à jour
            str_sql_id_fournisseur = """
                             SELECT f.nom_fournisseur, mail.nom_mail, tel.num_telephone, a.nom_rue_adresse, a.ville_adresse, a.npa_adresse
                             FROM t_fournisseur AS f
                             JOIN t_mail_avoir_fournisseur AS m ON m.fk_fournisseur = f.id_fournisseur
                             JOIN t_mail AS mail ON m.fk_mail = mail.id_mail
                             JOIN t_telephone_avoir_fournisseur AS t ON t.fk_fournisseur = f.id_fournisseur
                             JOIN t_telephone AS tel ON t.fk_telephone = tel.id_telephone
                             JOIN t_adresse_etre_fournisseur AS af ON af.fk_fournisseur = f.id_fournisseur
                             JOIN t_adresse AS a ON af.fk_adresse = a.id_adresse
                             WHERE f.id_fournisseur = %(value_id_fournisseur)s
                             """

            str_sql_id_fournisseur = """
                            SELECT f.nom_fournisseur
                            FROM t_fournisseur AS f
                            WHERE f.id_fournisseur = %(value_id_fournisseur)s
                            """
            str_sql_id_fournisseur_mail = """
                                        SELECT mail.nom_mail
                                        FROM t_mail_avoir_fournisseur AS m
                                        JOIN t_mail AS mail ON m.fk_mail = mail.id_mail
                                        WHERE m.fk_fournisseur = %(value_id_fournisseur)s
                                        """
            str_sql_id_fournisseur_adresse = """
                            SELECT a.nom_rue_adresse, a.ville_adresse, a.npa_adresse
                            FROM t_adresse_etre_fournisseur AS af
                            JOIN t_adresse AS a ON af.fk_adresse = a.id_adresse
                            WHERE af.fk_fournisseur = %(value_id_fournisseur)s
                            """
            str_sql_id_fournisseur_telephone = """
                            SELECT tel.id_telephone, tel.num_telephone
                            FROM t_telephone_avoir_fournisseur AS t
                            JOIN t_telephone AS tel ON t.fk_telephone = tel.id_telephone
                            WHERE t.fk_fournisseur = %(value_id_fournisseur)s
                            """


            valeur_select_dictionnaire = {"value_id_fournisseur": id_fournisseur_update}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_fournisseur, valeur_select_dictionnaire)
                data_fournisseur = mybd_conn.fetchone()
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_fournisseur_mail, valeur_select_dictionnaire)
                data_fournisseur_mail = mybd_conn.fetchall()
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_fournisseur_adresse, valeur_select_dictionnaire)
                data_fournisseur_addresse = mybd_conn.fetchall()
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_fournisseur_telephone, valeur_select_dictionnaire)
                data_fournisseur_tel = mybd_conn.fetchall()

            if data_fournisseur :
                form_update.nom_fournisseur_update_wtf.data = data_fournisseur["nom_fournisseur"]
                form_update.email_fournisseur_wtf_essai.data = data_fournisseur_mail
                form_update.telephone_fournisseur_wtf_essai.data = data_fournisseur_tel
                form_update.adresse.data = data_fournisseur_addresse

                # Gestion du sous-formulaire de téléphone
                telephones = []
                for tel in data_fournisseur_tel:
                    tel_form = FormWTFTelephone()
                    tel_form.telephone.id = tel["id_telephone"]
                    tel_form.telephone.name = "telephone"+str(tel["id_telephone"])
                    tel_form.telephone.data = tel["num_telephone"]
                    telephones.append(tel_form)
                form_update.telephones = telephones

                form_update.nom_rue_adresse.data = "" #data_fournisseur["nom_rue_adresse"]
                form_update.ville_fournisseur.data = "" #data_fournisseur["ville_adresse"]
                form_update.code_postal_fournisseur.data = "" # data_fournisseur["npa_adresse"]
            else:
                flash("Fournisseur introuvable.", "error")
                # return redirect(url_for('fournisseur_afficher', order_by="ASC", id_fournisseur_sel=id_fournisseur_update))

    except Exception as Exception_fournisseur_update_wtf:
        raise ExceptionFournisseurUpdateWtf(
            f"fichier : {Path(__file__).name}  ;  "
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

    id_fournisseur_delete = request.values['id_fournisseur_btn_delete_html']

    form_delete = FormWTFDeleteFournisseur()

    try:
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("fournisseur_afficher", order_by="ASC", id_fournisseur_sel=0))

            if form_delete.submit_btn_conf_del.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("SELECT * FROM t_fournisseur WHERE id_fournisseur = %s", (id_fournisseur_delete,))
                    data_boisson_attribue_fournisseur_delete = mconn_bd.fetchall()

                flash("Effacer le fournisseur de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                with DBconnection() as mconn_bd:
                    # Supprimer les enregistrements dans la table t_adresse_etre_fournisseur
                    mconn_bd.execute("DELETE FROM t_adresse_etre_fournisseur WHERE fk_fournisseur = %s", (id_fournisseur_delete,))

                    # Supprimer les enregistrements dans la table t_boisson_acheter_fournisseur
                    mconn_bd.execute("DELETE FROM t_boisson_acheter_fournisseur WHERE fk_fournisseur = %s", (id_fournisseur_delete,))

                    # Supprimer les enregistrements dans la table t_boisson_retourner_fournisseur
                    mconn_bd.execute("DELETE FROM t_boisson_retourner_fournisseur WHERE fk_fournisseur = %s", (id_fournisseur_delete,))

                    # Supprimer les enregistrements dans la table t_mail_avoir_fournisseur
                    mconn_bd.execute("DELETE FROM t_mail_avoir_fournisseur WHERE fk_fournisseur = %s", (id_fournisseur_delete,))

                    # Supprimer les enregistrements dans la table t_telephone_avoir_fournisseur
                    mconn_bd.execute("DELETE FROM t_telephone_avoir_fournisseur WHERE fk_fournisseur = %s", (id_fournisseur_delete,))

                    # Ensuite, supprimer la ligne dans la table t_fournisseur
                    mconn_bd.execute("DELETE FROM t_fournisseur WHERE id_fournisseur = %s", (id_fournisseur_delete,))

                flash("Fournisseur définitivement effacé !!", "success")
                return redirect(url_for('fournisseur_afficher', order_by="ASC", id_fournisseur_sel=0))

        if request.method == "GET":
            with DBconnection() as mconn_bd:
                mconn_bd.execute("SELECT * FROM t_boisson_acheter_fournisseur "
                                 "INNER JOIN t_boisson ON t_boisson_acheter_fournisseur.fk_boisson = t_boisson.id_boisson "
                                 "INNER JOIN t_fournisseur ON t_boisson_acheter_fournisseur.fk_fournisseur = t_fournisseur.id_fournisseur "
                                 "WHERE fk_fournisseur = %s", (id_fournisseur_delete,))
                data_boisson_attribue_fournisseur_delete = mconn_bd.fetchall()

                mconn_bd.execute("SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur WHERE id_fournisseur = %s", (id_fournisseur_delete,))
                data_nom_fournisseur = mconn_bd.fetchone()

            form_delete.nom_fournisseur_delete_wtf.data = data_nom_fournisseur["nom_fournisseur"]
            btn_submit_del = False



    except Exception as Exception_fournisseur_delete_wtf:

        raise Exception("Erreur dans la fonction fournisseur_delete_wtf : " + str(Exception_fournisseur_delete_wtf))

    return render_template("Fournisseur/fournisseur_delete_wtf.html",

                           form_delete=form_delete,

                           btn_submit_del=btn_submit_del,

                           data_boisson_associes=data_boisson_attribue_fournisseur_delete)