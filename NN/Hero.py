class Hero:

    def __init__(self, JHero):
        self.id = JHero['neural_id']
        self.heroId = JHero['api_id']
        self.displayName = JHero['display_name']