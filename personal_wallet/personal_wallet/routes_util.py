class ProjectURLs:

    def __init__(self):

        # general project urls constants
        self.__list_view_constant = 'list/'
        self.__create_view_constant = 'create/'
        self.__detail_view_constant = 'detail/'
        self.__update_view_constant = 'update/'
        self.__delete_view_constant = 'delete/'
        self.__frontend_first_lookup_constant = '{1}/'
        self.__frontend_second_lookup_constant = '{2}/'
        self.__url_name_sep = '-'

        # project urls
        self.__admin_url = 'admin/'
        self.__get_all_project_urls = 'get_urls/'

        # users urls
        self.__users_base_url = 'users/'
        self.__users_registration_url = 'register/'
        self.__users_obtain_token_url = 'token/'
        self.__users_refresh_token_url = 'token/refresh/'

        # wallets urls
        self.__wallets_base_url = 'wallets/'
        self.__wallets_id_lookup = '<int:wallet_id>/'

        # expenses urls
        self.__expenses_base_url = 'expenses/'
        self.__expenses_id_lookup = '<int:expense_id>/'
        self.__expenses_type_lookup = '<str:type>/'

        # incomes urls
        self.__incomes_base_url = 'incomes/'
        self.__incomes_id_lookup = '<int:income_id>/'

        # choices urls
        self.__currency_choices_url = 'currency_choices/'
        self.__expenses_choices_url = 'expenses_choices/'
        self.__incomes_choices_url = 'incomes_choices/'

        # statistics urls
        self.__statistics_base_url = 'statistics/'
        self.__statistic_total_url = 'total/'
        self.__statistic_max_url = 'max/'
        self.__statistics_percentage_url = 'percentage/'
        self.__statistics_expenses_total_url_name = 'expenses-total'
        self.__statistics_incomes_total_url_name = 'incomes-total'
        self.__statistics_expenses_max_url_name = 'expenses-max'
        self.__statistics_incomes_max_url_name = 'incomes-max'
        self.__statistics_expenses_percentage_url_name = 'expenses-percentage'
        self.__statistics_incomes_percentage_url_name = 'incomes-percentage'
        self.__statistics_expenses_by_type_name_addition = 'expenses-by-type'
        self.__statistics_incomes_by_type_name_addition = 'incomes-by-type'

        # users app
        self.__users_app_name = 'users'

        # wallets app
        self.__wallets_app_name = 'wallets'

        # statistics app
        self.__statistics_app_name = 'wallet_statistics'

        self.__urls_file_name = 'urls'

    # project urls
    def admin_url(self):
        return self.__admin_url

    def admin_url_name(self):
        return self.__admin_url[:-1]

    def get_urls_url(self):
        return self.__get_all_project_urls

    def get_urls_url_name(self):
        return self.__get_all_project_urls[:-1]

    # users urls
    def users_base_url(self):
        return self.__users_base_url

    def users_registration_url(self, for_frontend: bool):
        if for_frontend:
            return self.__users_base_url + self.__users_registration_url
        return self.__users_registration_url

    def users_registration_url_name(self):
        return self.__users_base_url[:-1] + self.__url_name_sep + self.__users_registration_url[:-1]

    def users_obtain_token_url(self, for_frontend: bool):
        if for_frontend:
            return self.__users_base_url + self.__users_obtain_token_url
        return self.__users_obtain_token_url

    def users_obtain_token_url_name(self):
        return self.__users_base_url[:-1] + '-obtain-' + self.__users_obtain_token_url[:-1]

    def users_refresh_token_url(self, for_frontend: bool):
        if for_frontend:
            return self.__users_base_url + self.__users_refresh_token_url
        return self.__users_refresh_token_url

    def users_refresh_token_url_name(self):
        return self.__users_base_url[:-1] + '-refresh-' + self.__users_refresh_token_url[:-9]

    # wallets urls
    def wallets_base_url(self):
        return self.__wallets_base_url

    def wallets_create_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__create_view_constant
        return self.__create_view_constant

    def wallets_create_url_name(self):
        return self.__wallets_base_url[:-1] + self.__url_name_sep + self.__create_view_constant[:-1]

    def wallets_detail_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__detail_view_constant + self.__frontend_first_lookup_constant
        return self.__detail_view_constant + self.__wallets_id_lookup

    def wallets_detail_url_name(self):
        return self.__wallets_base_url[:-1] + self.__url_name_sep + self.__detail_view_constant[:-1]

    def wallets_update_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__update_view_constant + self.__frontend_first_lookup_constant
        return self.__update_view_constant + self.__wallets_id_lookup

    def wallets_update_url_name(self):
        return self.__wallets_base_url[:-1] + self.__url_name_sep + self.__update_view_constant[:-1]

    def wallets_delete_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__delete_view_constant + self.__frontend_first_lookup_constant
        return self.__delete_view_constant + self.__wallets_id_lookup

    def wallets_delete_url_name(self):
        return self.__wallets_base_url[:-1] + self.__url_name_sep + self.__delete_view_constant[:-1]

    def wallets_list_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__list_view_constant
        return self.__list_view_constant

    def wallets_list_url_name(self):
        return self.__wallets_base_url[:-1] + self.__url_name_sep + self.__list_view_constant[:-1]

    # expense urls
    def expenses_create_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__frontend_first_lookup_constant + self.__expenses_base_url + \
                   self.__create_view_constant
        return self.__wallets_id_lookup + self.__expenses_base_url + self.__create_view_constant

    def expenses_create_url_name(self):
        return self.__expenses_base_url[:-1] + self.__url_name_sep + self.__create_view_constant[:-1]

    def expenses_delete_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__frontend_first_lookup_constant + self.__expenses_base_url + \
                   self.__delete_view_constant + self.__frontend_second_lookup_constant
        return self.__wallets_id_lookup + self.__expenses_base_url + self.__delete_view_constant + \
            self.__expenses_id_lookup

    def expenses_delete_url_name(self):
        return self.__expenses_base_url[:-1] + self.__url_name_sep + self.__delete_view_constant

    def expenses_list_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__frontend_first_lookup_constant + self.__expenses_base_url + \
                   self.__list_view_constant
        return self.__wallets_id_lookup + self.__expenses_base_url + self.__list_view_constant

    def expenses_list_url_name(self):
        return self.__expenses_base_url[:-1] + self.__url_name_sep + self.__list_view_constant[:-1]

    # incomes urls
    def incomes_create_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__frontend_first_lookup_constant + self.__incomes_base_url + \
                   self.__create_view_constant
        return self.__wallets_id_lookup + self.__incomes_base_url + self.__create_view_constant

    def incomes_create_url_name(self):
        return self.__incomes_base_url[:-1] + self.__url_name_sep + self.__create_view_constant[:-1]

    def incomes_delete_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__frontend_first_lookup_constant + self.__incomes_base_url + \
                   self.__delete_view_constant + self.__frontend_second_lookup_constant
        return self.__wallets_id_lookup + self.__incomes_base_url + self.__delete_view_constant + \
            self.__incomes_id_lookup

    def incomes_delete_url_name(self):
        return self.__incomes_base_url[:-1] + self.__url_name_sep + self.__delete_view_constant

    def incomes_list_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__frontend_first_lookup_constant + self.__incomes_base_url + \
                   self.__list_view_constant
        return self.__wallets_id_lookup + self.__incomes_base_url + self.__list_view_constant

    def incomes_list_url_name(self):
        return self.__incomes_base_url[:-1] + self.__url_name_sep + self.__list_view_constant[:-1]

    def currency_choices_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__currency_choices_url
        return self.__currency_choices_url

    def currency_choices_url_name(self):
        return self.__currency_choices_url[:-9] + self.__url_name_sep + self.__currency_choices_url[9:-1]

    def expenses_choices_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__expenses_base_url + self.__expenses_choices_url
        return self.__expenses_base_url + self.__expenses_choices_url

    def expenses_choices_url_name(self):
        return self.__expenses_choices_url[:-9] + self.__url_name_sep + self.__expenses_choices_url[9:-1]

    def incomes_choices_url(self, for_frontend: bool):
        if for_frontend:
            return self.__wallets_base_url + self.__incomes_base_url + self.__incomes_choices_url
        return self.__incomes_base_url + self.__incomes_choices_url

    def incomes_choices_url_name(self):
        return self.__incomes_choices_url[:-9] + self.__url_name_sep + self.__incomes_choices_url[8:-1]

    # statistic urls
    def statistics_base_url(self):
        return self.__statistics_base_url

    def statistics_expenses_by_type_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__expenses_base_url + self.__frontend_first_lookup_constant + \
                   self.__frontend_second_lookup_constant
        return self.__expenses_base_url + self.__wallets_id_lookup + \
            self.__expenses_type_lookup

    def statistics_expenses_by_type_url_name(self):
        return self.__statistics_base_url[:-1] + self.__url_name_sep + \
               self.__statistics_expenses_by_type_name_addition

    def statistics_incomes_by_type_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__incomes_base_url + self.__frontend_first_lookup_constant + \
                   self.__frontend_second_lookup_constant
        return self.__incomes_base_url + self.__wallets_id_lookup + \
            self.__expenses_type_lookup

    def statistics_incomes_by_type_url_name(self):
        return self.__statistics_base_url[:-1] + self.__url_name_sep + \
               self.__statistics_incomes_by_type_name_addition

    def statistics_expenses_total_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__statistic_total_url + self.__expenses_base_url + \
                   self.__frontend_first_lookup_constant
        return self.__statistic_total_url + self.__expenses_base_url + self.__wallets_id_lookup

    def statistics_expenses_total_url_name(self):
        return self.__statistics_expenses_total_url_name

    def statistics_incomes_total_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__statistic_total_url + self.__incomes_base_url + \
                   self.__frontend_first_lookup_constant
        return self.__statistic_total_url + self.__incomes_base_url + self.__wallets_id_lookup

    def statistics_incomes_total_url_name(self):
        return self.__statistics_incomes_total_url_name

    def statistics_expenses_max_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__statistic_max_url + self.__expenses_base_url + \
                   self.__frontend_first_lookup_constant
        return self.__statistic_max_url + self.__expenses_base_url + self.__wallets_id_lookup

    def statistics_expenses_max_url_name(self):
        return self.__statistics_expenses_max_url_name

    def statistics_incomes_max_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__statistic_max_url + self.__incomes_base_url + \
                   self.__frontend_first_lookup_constant
        return self.__statistic_max_url + self.__incomes_base_url + self.__wallets_id_lookup

    def statistics_incomes_max_url_name(self):
        return self.__statistics_incomes_max_url_name

    def statistics_expenses_percentage_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__statistics_percentage_url + self.__expenses_base_url + \
                   self.__frontend_first_lookup_constant
        return self.__statistics_percentage_url + self.__expenses_base_url + self.__wallets_id_lookup

    def statistics_expenses_percentage_url_name(self):
        return self.__statistics_expenses_percentage_url_name

    def statistics_incomes_percentage_url(self, for_frontend: bool):
        if for_frontend:
            return self.__statistics_base_url + self.__statistics_percentage_url + self.__incomes_base_url + \
                   self.__frontend_first_lookup_constant
        return self.__statistics_percentage_url + self.__incomes_base_url + self.__wallets_id_lookup

    def statistics_incomes_percentage_url_name(self):
        return self.__statistics_incomes_percentage_url_name

    def get_all_general_project_urls(self):
        general_project_urls_key = 'general_project_urls'
        return {
            general_project_urls_key: [
                {self.admin_url_name(): self.__admin_url},
                {self.get_urls_url_name(): self.__get_all_project_urls}
            ]
        }

    def get_all_users_urls(self):
        users_urls_key = 'users_urls'
        return {
            users_urls_key: [
                {self.users_registration_url_name(): self.users_registration_url(for_frontend=True)},
                {self.users_obtain_token_url_name(): self.users_obtain_token_url(for_frontend=True)},
                {self.users_refresh_token_url_name(): self.users_refresh_token_url(for_frontend=True)}
            ]
        }

    def get_all_wallets_urls(self):
        wallets_urls_key = 'wallets'
        return {
            wallets_urls_key: [
                {self.__create_view_constant[:-1]: self.wallets_create_url(for_frontend=True)},
                {self.__detail_view_constant[:-1]: self.wallets_detail_url(for_frontend=True)},
                {self.__update_view_constant[:-1]: self.wallets_update_url(for_frontend=True)},
                {self.__delete_view_constant[:-1]: self.wallets_delete_url(for_frontend=True)},
                {self.__list_view_constant[:-1]: self.wallets_list_url(for_frontend=True)},
                {self.currency_choices_url_name(): self.currency_choices_url(for_frontend=True)}
            ]
        }

    def get_all_expenses_urls(self):
        expenses_urls_key = 'expenses'
        return {
            expenses_urls_key: [
                {self.__create_view_constant[:-1]: self.expenses_create_url(for_frontend=True)},
                {self.__delete_view_constant[:-1]: self.expenses_delete_url(for_frontend=True)},
                {self.__list_view_constant[:-1]: self.expenses_list_url(for_frontend=True)},
                {self.expenses_choices_url_name(): self.expenses_choices_url(for_frontend=True)}
            ]
        }

    def get_all_incomes_urls(self):
        incomes_urls_key = 'incomes'
        return {
            incomes_urls_key: [
                {self.__create_view_constant[:-1]: self.incomes_create_url(for_frontend=True)},
                {self.__delete_view_constant[:-1]: self.incomes_delete_url(for_frontend=True)},
                {self.__list_view_constant[:-1]: self.incomes_list_url(for_frontend=True)},
                {self.incomes_choices_url_name(): self.incomes_choices_url(for_frontend=True)}
            ]
        }

    def get_all_statistics_urls(self):
        statistics_urls_key = 'statistics'
        return {
            statistics_urls_key: [
                {self.statistics_expenses_by_type_url_name(): self.statistics_expenses_by_type_url(for_frontend=True)},
                {self.statistics_incomes_by_type_url_name(): self.statistics_expenses_by_type_url(for_frontend=True)},
                {self.statistics_expenses_total_url_name(): self.statistics_expenses_total_url(for_frontend=True)},
                {self.statistics_incomes_total_url_name(): self.statistics_incomes_total_url(for_frontend=True)},
                {self.statistics_expenses_max_url_name(): self.statistics_expenses_max_url(for_frontend=True)},
                {self.statistics_incomes_max_url_name(): self.statistics_incomes_max_url(for_frontend=True)},
                {self.statistics_expenses_percentage_url_name(): self.statistics_expenses_percentage_url(
                    for_frontend=True)},
                {self.statistics_incomes_percentage_url_name(): self.statistics_incomes_percentage_url(
                    for_frontend=True)},
            ]
        }

    def get_all_project_urls(self):
        urls_key = 'urls'
        return {
            urls_key: [
                self.get_all_general_project_urls(),
                self.get_all_users_urls(),
                self.get_all_wallets_urls(),
                self.get_all_expenses_urls(),
                self.get_all_incomes_urls(),
                self.get_all_statistics_urls()
            ]
        }

    def get_users_url_file_name(self):
        return self.__users_app_name + '.' + self.__urls_file_name

    def get_wallets_url_file_name(self):
        return self.__wallets_app_name + '.' + self.__urls_file_name

    def get_statistics_url_file_name(self):
        return self.__statistics_app_name + '.' + self.__urls_file_name


routes_util = ProjectURLs()
