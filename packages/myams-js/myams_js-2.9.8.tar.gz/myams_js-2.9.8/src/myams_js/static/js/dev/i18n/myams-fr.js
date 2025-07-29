/* global MyAMS, jQuery */

(function($) {

	$.extend(MyAMS.i18n, {

		language: 'fr',

		INFO: "Information",
		WARNING: "!! ATTENTION !!",
		ERROR: "ERREUR: ",

		LOADING: "Chargement en cours...",
		PROGRESS: "Traitement en cours...",

		WAIT: "Veuillez patienter...",
		FORM_SUBMITTED: "Vous avez déjà soumis ce formulaire !",
		NO_SERVER_RESPONSE: "Pas de réponse du serveur !",

		ERROR_OCCURED: "Une erreur s'est produite!",
		ERRORS_OCCURED: "Des erreurs se sont produites !",

		BAD_LOGIN_TITLE: "Paramètres de connexion incorrects !",
		BAD_LOGIN_MESSAGE:
			"Les paramètres de connexion que vous avez indiqués n'ont pas permis d'établir la " +
			"connexion ; veuillez vérifier ces paramètres, ou contactez un administrateur.",

		CONFIRM: "Confirmer",
		CONFIRM_REMOVE:
			"La suppression de ce contenu ne pourra pas être annulée. Confirmez-vous ?",

		BTN_OK: "OK",
		BTN_CANCEL: "Annuler",
		BTN_YES: "Oui",
		BTN_NO: "Non",

		CLIPBOARD_COPY: "Copiez ce contenu dans le presse-papier avec Ctrl+C, puis Entrée",
		CLIPBOARD_CHARACTER_COPY_OK: "Le caractère a été déposé dans le presse-papier.",
		CLIPBOARD_TEXT_COPY_OK: "Le texte a été copié dans le presse-papier.",

		FORM_CHANGED_WARNING:
			"Des modifications n'ont pas été enregistrées. Ces modifications seront perdues si " +
			"vous quittez cette page.",
		DELETE_WARNING: "Cette suppression ne pourra pas être annulée. La confirmez-vous ?",
		NO_UPDATE: "Aucune modification n'a été enregistrée.",
		DATA_UPDATED: "Vos modifications ont été enregistrées.",

		HOME: "Accueil",
		LOGOUT: "Déconnexion ?",
		LOGOUT_COMMENT:
			"Vous pourrez améliorer votre sécurité en fermant cette fenêtre après vous être " +
			"déconnecté.<br />Confirmez-vous la déconnexion ?",

		LAST_UPDATE: "Dernière mise à jour : ",

		DT_COLUMNS: "Colonnes",

		NO_SELECTED_VALUE: "Pas de valeur sélectionnée",

		// Plug-ins translations
		plugins: {

			// Datatables plug-in translations
			datatables: {
				processing:     "Traitement en cours...",
				search:         "",
				searchPlaceholder: "Filtrer...",
				lengthMenu:     "_MENU_ &eacute;l&eacute;ments par page",
				info:           "Affichage des &eacute;l&eacute;ments _START_ &agrave; _END_ sur _TOTAL_",
				infoEmpty:      "Aucun &eacute;l&eacute;ment &agrave; afficher",
				infoFiltered:   "(sur un total de _MAX_)",
				infoPostFix:    "",
				loadingRecords: "Chargement en cours...",
				zeroRecords:    "Aucun &eacute;l&eacute;ment &agrave; afficher",
				emptyTable:     "Aucune donnée disponible dans le tableau",
				paginate: {
					first:      "Premier",
					previous:   "Pr&eacute;c&eacute;dent",
					next:       "Suivant",
					last:       "Dernier"
				},
				columns:        "Colonnes",
				buttons: {
					copy:       "Copier",
					copyTitle:  "Copie dans le presse-papiers",
					copySuccess: {
						1:      "Une ligne copiée dans le presse-papiers.",
						_:      "%d lignes copiées dans le presse-papiers."
					},
					print:      "Imprimer",
					colvis:     "Colonnes"
				},
				searchPanes: {
					emptyPanes: "Pas de filtre de recherche !"
				},
				aria: {
					sortAscending:  ": activer pour trier la colonne par ordre croissant",
					sortDescending: ": activer pour trier la colonne par ordre décroissant"
				}
			}
		}
	});

})(jQuery);