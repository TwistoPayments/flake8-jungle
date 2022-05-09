class Foo:
    def test(self):
        if not (
            self.site.get(SiteFeaturesService).get_split_flag_version(self.account)
            and (
                self.account.current_plan.plan
                in (self.account.PLAN_STANDARD, self.account.PLAN_PREMIUM)
                or not self.site.is_cz
            )
        ):
            return "abc"
