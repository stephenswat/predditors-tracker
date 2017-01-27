from social_core.backends.eveonline import EVEOnlineOAuth2


class CustomEVEOnlineOAuth2(EVEOnlineOAuth2):
    def get_scope(self):
        scope = super(EVEOnlineOAuth2, self).get_scope()

        if 'alt' in self.data:
            scope = scope + ['characterLocationRead', 'esi-location.read_location.v1', 'esi-location.read_ship_type.v1']

        return scope
