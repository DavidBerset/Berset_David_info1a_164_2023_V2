"""
    Fichier : gestion_boisson_fournisseur_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les Boissons et les Fournisseurs.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

"""
    Nom : boisson_fournisseur_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /boisson_fournisseur_afficher

    But : Afficher les Boissons avec les Fournisseurs associés pour chaque boisson.

    Paramètres : id_fournisseur_sel = 0 >> toutes les Boisson.
                 id_fournisseur_sel = "n" affiche la boisson dont l'id est "n"

"""


@app.route("/boisson_fournisseur_afficher/<int:id_boisson_sel>", methods=['GET', 'POST'])
def boisson_fournisseur_afficher(id_boisson_sel):
    print(" boisson_fournisseur_afficher id_boisson_sel ", id_boisson_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                # sous requete par de t_boisson et compte la quantité stockée depuis cette requête on va rechercher la liste des fournisseurs par boisson
                strsql_fournisseur_boisson_afficher_data = """
                    SELECT 
                        id_boisson, 
                        nom_boisson, 
                        type_boisson, 
                        prix_vente_boisson, 
                        cover_link_boisson, 
                        code_barre_boisson, 
                        stock_boisson AS Stock
                    FROM t_boisson 
                    LEFT JOIN t_boisson_acheter_fournisseur ON id_boisson = t_boisson_acheter_fournisseur.fk_boisson
                    LEFT JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_boisson_acheter_fournisseur.fk_fournisseur
                """
                if id_boisson_sel == 0:
                    # le paramètre 0 permet d'afficher tous les Boissons
                    # Sinon le paramètre représente la valeur de l'id de la boisson
                    mc_afficher.execute(strsql_fournisseur_boisson_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id de la boisson sélectionnée avec un nom de variable
                    valeur_id_boisson_selected_dictionnaire = {"value_id_boisson_selected": id_boisson_sel}
                    # En MySql, l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_fournisseur_boisson_afficher_data += """ HAVING id_boisson= %(value_id_boisson_selected)s"""

                    mc_afficher.execute(strsql_fournisseur_boisson_afficher_data, valeur_id_boisson_selected_dictionnaire)

                # Récupère les données de la requête.
                data_fournisseur_boisson_afficher = mc_afficher.fetchall()
                print("data_fournisseur ", data_fournisseur_boisson_afficher, " Type : ", type(data_fournisseur_boisson_afficher))

                # Différencier les messages.
                if not data_fournisseur_boisson_afficher and id_boisson_sel == 0:
                    flash("""La table "t_boisson" est vide. !""", "warning")
                elif not data_fournisseur_boisson_afficher and id_boisson_sel > 0:
                    # Si l'utilisateur change l'id_boisson dans l'URL et qu'il ne correspond à aucune boisson
                    flash(f"La boisson {id_boisson_sel} demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données Boisson et Fournisseur affichées !!", "success")

        except Exception as Exception_boisson_fournisseur_afficher:
            raise ExceptionBoissonFournisseurAfficher(f"fichier : {Path(__file__).name}  ;  {boisson_fournisseur_afficher.__name__} ;"
                                               f"{Exception_boisson_fournisseur_afficher}")

    print("boisson_fournisseur_afficher  ", data_fournisseur_boisson_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("Boisson_Fournisseur/boisson_fournisseur_afficher.html", data=data_fournisseur_boisson_afficher)


"""
    nom: edit_fournisseur_boisson_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les Fournisseurs de la boisson sélectionné par le bouton "MODIFIER" de "boisson_fournisseur_afficher.html"

    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les Fournisseur contenus dans la "t_fournisseur".
    2) Les Fournisseur attribués au boisson selectionné.
    3) Les Fournisseur non-attribués au boisson sélectionné.

    On signale les erreurs importantes

"""


@app.route("/edit_fournisseur_boisson_selected", methods=['GET', 'POST'])
def edit_fournisseur_boisson_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_fournisseur_afficher = """SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur ORDER BY id_fournisseur ASC"""
                mc_afficher.execute(strsql_fournisseur_afficher)
            data_fournisseur_all = mc_afficher.fetchall()
            print("dans edit_fournisseur_boisson_selected ---> data_fournisseur_all", data_fournisseur_all)

            # Récupère la valeur de "id_boisson" du formulaire html "boisson_fournisseur_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_boisson"
            # grâce à la variable "id_film_genres_edit_html" dans le fichier "boisson_fournisseur_afficher.html"
            # href="{{ url_for('edit_fournisseur_boisson_selected', id_film_genres_edit_html=row.id_boisson) }}"
            id_boisson_fournisseur_edit = request.values['id_film_genres_edit_html']

            # Mémorise l'id de la boisson dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_boisson_fournisseur_edit'] = id_boisson_fournisseur_edit

            # Constitution d'un dictionnaire pour associer l'id de la boisson sélectionné avec un nom de variable
            valeur_id_boisson_selected_dictionnaire = {"value_id_boisson_selected": id_boisson_fournisseur_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction fournisseur_boisson_afficher_data
            # 1) Sélection de la boisson choisi
            # 2) Sélection des Fournisseur "déjà" attribués pour la boisson.
            # 3) Sélection des Fournisseur "pas encore" attribués pour la boisson choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "fournisseur_boisson_afficher_data"
            data_fournisseur_boisson_selected, data_fournisseur_boisson_non_attribues, data_fournisseur_boisson_attribues = \
                fournisseur_boisson_afficher_data(valeur_id_boisson_selected_dictionnaire)

            print(data_fournisseur_boisson_selected)
            lst_data_boisson_selected = [item['id_boisson'] for item in data_fournisseur_boisson_selected]
            print("lst_data_boisson_selected  ", lst_data_boisson_selected,
                  type(lst_data_boisson_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les Fournisseur qui ne sont pas encore sélectionnés.
            lst_data_fournisseur_boisson_non_attribues = [item['id_fournisseur'] for item in data_fournisseur_boisson_non_attribues]
            session['session_lst_data_fournisseur_boisson_non_attribues'] = lst_data_fournisseur_boisson_non_attribues
            print("lst_data_fournisseur_boisson_non_attribues  ", lst_data_fournisseur_boisson_non_attribues,
                  type(lst_data_fournisseur_boisson_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les Fournisseur qui sont déjà sélectionnés.
            lst_data_fournisseur_boisson_old_attribues = [item['id_fournisseur'] for item in data_fournisseur_boisson_attribues]
            session['session_lst_data_fournisseur_boisson_old_attribues'] = lst_data_fournisseur_boisson_old_attribues
            print("lst_data_fournisseur_boisson_old_attribues  ", lst_data_fournisseur_boisson_old_attribues,
                  type(lst_data_fournisseur_boisson_old_attribues))

            print(" data data_fournisseur_boisson_selected", data_fournisseur_boisson_selected, "type ", type(data_fournisseur_boisson_selected))
            print(" data data_fournisseur_boisson_non_attribues ", data_fournisseur_boisson_non_attribues, "type ",
                  type(data_fournisseur_boisson_non_attribues))
            print(" data_fournisseur_boisson_attribues ", data_fournisseur_boisson_attribues, "type ",
                  type(data_fournisseur_boisson_attribues))

            # Extrait les valeurs contenues dans la table "t_fournisseur", colonne "nom_fournisseur"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_fournisseur
            lst_data_fournisseur_boisson_non_attribues = [item['nom_fournisseur'] for item in data_fournisseur_boisson_non_attribues]
            print("lst_all_fournisseur gf_edit_fournisseur_boisson_selected ", lst_data_fournisseur_boisson_non_attribues,
                  type(lst_data_fournisseur_boisson_non_attribues))

        except Exception as Exception_edit_fournisseur_boisson_selected:
            raise ExceptionEditFournisseurBoissonSelected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_fournisseur_boisson_selected.__name__} ; "
                                                 f"{Exception_edit_fournisseur_boisson_selected}")

    return render_template("Boisson_Fournisseur/boisson_fournisseur_modifier_tags_dropbox.html",
                           data_fournisseur=data_fournisseur_all,
                           data_boisson_selected=data_fournisseur_boisson_selected,
                           data_fournisseur_attribues=data_fournisseur_boisson_attribues,
                           data_fournisseur_non_attribues=data_fournisseur_boisson_non_attribues)


"""
    nom: update_fournisseur_boisson_selected

    Récupère la liste de tous les Fournisseur de la boisson sélectionné par le bouton "MODIFIER" de "boisson_fournisseur_afficher.html"

    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les Fournisseur contenus dans la "t_fournisseur".
    2) Les Fournisseur attribués à la boisson selectionné.
    3) Les Fournisseur non-attribués à la boisson sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_fournisseur_boisson_selected", methods=['GET', 'POST'])
def update_fournisseur_boisson_selected():
    if request.method == "POST":
        try:
            # Récupère l'id de la boisson sélectionné
            id_boisson_selected = session['session_id_boisson_fournisseur_edit']
            print("session['session_id_boisson_fournisseur_edit'] ", session['session_id_boisson_fournisseur_edit'])

            # Récupère la liste des Fournisseur qui ne sont pas associés à la boisson sélectionné.
            old_lst_data_fournisseur_boisson_non_attribues = session['session_lst_data_fournisseur_boisson_non_attribues']
            print("old_lst_data_fournisseur_boisson_non_attribues ", old_lst_data_fournisseur_boisson_non_attribues)

            # Récupère la liste des Fournisseur qui sont associés à la boisson sélectionné.
            old_lst_data_fournisseur_boisson_attribues = session['session_lst_data_fournisseur_boisson_old_attribues']
            print("old_lst_data_fournisseur_boisson_old_attribues ", old_lst_data_fournisseur_boisson_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme Fournisseur dans le composant "tags-selector-tagselect"
            # dans le fichier "fournisseur_boisson_modifier_tags_dropbox.html"
            new_lst_str_fournisseur_boisson = request.form.getlist('name_select_tags')
            print("new_lst_str_fournisseur_boisson ", new_lst_str_fournisseur_boisson)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_fournisseur_boisson_old = list(map(int, new_lst_str_fournisseur_boisson))
            print("new_lst_fournisseur_boisson ", new_lst_int_fournisseur_boisson_old, "type new_lst_fournisseur_boisson ",
                  type(new_lst_int_fournisseur_boisson_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_fournisseur" qui doivent être effacés de la table intermédiaire "t_boisson_acheter_fournisseur".
            lst_diff_fournisseur_delete_b = list(set(old_lst_data_fournisseur_boisson_attribues) -
                                            set(new_lst_int_fournisseur_boisson_old))
            print("lst_diff_fournisseur_delete_b ", lst_diff_fournisseur_delete_b)

            # Une liste de "id_fournisseur" qui doivent être ajoutés à la "t_boisson_acheter_fournisseur"
            lst_diff_fournisseur_insert_a = list(
                set(new_lst_int_fournisseur_boisson_old) - set(old_lst_data_fournisseur_boisson_attribues))
            print("lst_diff_fournisseur_insert_a ", lst_diff_fournisseur_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_boisson"/"id_boisson" et "fk_fournisseur"/"id_fournisseur" dans la "t_boisson_acheter_fournisseur"
            strsql_insert_fournisseur_boisson = """INSERT INTO t_boisson_acheter_fournisseur (id_boisson_acheter_fournisseur, fk_fournisseur, fk_boisson)
                                                    VALUES (NULL, %(value_fk_fournisseur)s, %(value_fk_boisson)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_boisson" et "id_fournisseur" dans la "t_boisson_acheter_fournisseur"
            strsql_delete_fournisseur_boisson = """DELETE FROM t_boisson_acheter_fournisseur WHERE fk_fournisseur = %(value_fk_fournisseur)s AND fk_boisson = %(value_fk_boisson)s"""

            with DBconnection() as mconn_bd:
                # Pour la boisson sélectionné, parcourir la liste des Fournisseur à INSÉRER dans la "t_boisson_acheter_fournisseur".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_fournisseur_ins in lst_diff_fournisseur_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id de la boisson sélectionné avec un nom de variable
                    # et "id_fournisseur_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_boisson_sel_fournisseur_sel_dictionnaire = {"value_fk_boisson": id_boisson_selected,
                                                               "value_fk_fournisseur": id_fournisseur_ins}

                    mconn_bd.execute(strsql_insert_fournisseur_boisson, valeurs_boisson_sel_fournisseur_sel_dictionnaire)

                # Pour la boisson sélectionné, parcourir la liste des Fournisseur à EFFACER dans la "t_boisson_acheter_fournisseur".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_fournisseur_del in lst_diff_fournisseur_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id de la boisson sélectionné avec un nom de variable
                    # et "id_fournisseur_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_boisson_sel_fournisseur_sel_dictionnaire = {"value_fk_boisson": id_boisson_selected,
                                                               "value_fk_fournisseur": id_fournisseur_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_fournisseur_boisson, valeurs_boisson_sel_fournisseur_sel_dictionnaire)

        except Exception as Exception_update_fournisseur_boisson_selected:
            raise ExceptionUpdateFournisseurBoissonSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{update_fournisseur_boisson_selected.__name__} ; "
                                                   f"{Exception_update_fournisseur_boisson_selected}")

    # Après cette mise à jour de la table intermédiaire "t_boisson_acheter_fournisseur",
    # on affiche les Boisson et le(urs) genre(s) associé(s).
    return redirect(url_for('boisson_fournisseur_afficher', id_boisson_sel=id_boisson_selected))


"""
    nom: fournisseur_boisson_afficher_data

    Récupère la liste de tous les Fournisseur de la boisson sélectionné par le bouton "MODIFIER" de "boisson_fournisseur_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des Fournisseur, ainsi l'utilisateur voit les Fournisseur à disposition

    On signale les erreurs importantes
"""


def fournisseur_boisson_afficher_data(valeur_id_boisson_selected_dict):
    print("valeur_id_boisson_selected_dict...", valeur_id_boisson_selected_dict)
    try:

        strsql_boisson_selected = """SELECT id_boisson, nom_boisson, type_boisson, prix_vente_boisson, cover_link_boisson, code_barre_boisson, GROUP_CONCAT(id_fournisseur) as BoissonFournisseur FROM t_boisson_acheter_fournisseur
                                        INNER JOIN t_boisson ON t_boisson.id_boisson = t_boisson_acheter_fournisseur.fk_boisson
                                        INNER JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_boisson_acheter_fournisseur.fk_fournisseur
                                        WHERE id_boisson = %(value_id_boisson_selected)s"""

        strsql_fournisseur_boisson_non_attribues = """SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur WHERE id_fournisseur not in(SELECT id_fournisseur as idGenresFilms FROM t_boisson_acheter_fournisseur
                                                    INNER JOIN t_boisson ON t_boisson.id_boisson = t_boisson_acheter_fournisseur.fk_boisson
                                                    INNER JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_boisson_acheter_fournisseur.fk_fournisseur
                                                    WHERE id_boisson = %(value_id_boisson_selected)s)"""

        strsql_fournisseur_boisson_attribues = """SELECT id_boisson, id_fournisseur, nom_fournisseur FROM t_boisson_acheter_fournisseur
                                            INNER JOIN t_boisson ON t_boisson.id_boisson = t_boisson_acheter_fournisseur.fk_boisson
                                            INNER JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_boisson_acheter_fournisseur.fk_fournisseur
                                            WHERE id_boisson = %(value_id_boisson_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_fournisseur_boisson_non_attribues, valeur_id_boisson_selected_dict)
            # Récupère les données de la requête.
            data_fournisseur_boisson_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("fournisseur_boisson_afficher_data ----> data_fournisseur_boisson_non_attribues ", data_fournisseur_boisson_non_attribues,
                  " Type : ",
                  type(data_fournisseur_boisson_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_boisson_selected, valeur_id_boisson_selected_dict)
            # Récupère les données de la requête.
            data_boisson_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_boisson_selected  ", data_boisson_selected, " Type : ", type(data_boisson_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_fournisseur_boisson_attribues, valeur_id_boisson_selected_dict)
            # Récupère les données de la requête.
            data_fournisseur_boisson_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_fournisseur_boisson_attribues ", data_fournisseur_boisson_attribues, " Type : ",
                  type(data_fournisseur_boisson_attribues))

            # Retourne les données des "SELECT"
            return data_boisson_selected, data_fournisseur_boisson_non_attribues, data_fournisseur_boisson_attribues

    except Exception as Exception_fournisseur_boisson_afficher_data:
        raise ExceptionFournisseurBoissonAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{fournisseur_boisson_afficher_data.__name__} ; "
                                               f"{Exception_fournisseur_boisson_afficher_data}")
