<template>
  <div>
    <div
      class="spacing bg-primary-color"
      v-if="this.$route.name == 'Landing'"
    />
    <b-navbar
      toggleable="md"
      type="light"
      class="bg-primary-color secondary-color"
    >
      <b-container>
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand to="/" @click="resetQuery">
          FactRank.
        </b-navbar-brand>
        <b-collapse is-nav id="nav_collapse">
          <b-navbar-nav class="ml-auto">
            <b-navbar-nav>
              <b-nav-item @click="resetQuery" to="/rank" exact>{{ $t("menu-bar.rank") }}</b-nav-item>
              <b-nav-item to="/tool">{{ $t("menu-bar.tool") }}</b-nav-item>
              <b-nav-item to="/about">{{ $t("menu-bar.about") }}</b-nav-item>
              <b-nav-item to="/press">{{ $t("menu-bar.press") }}</b-nav-item>
              <b-nav-item to="/api">{{ $t("menu-bar.api") }}</b-nav-item>
              <b-nav-item v-if="this.$i18n.locale.includes('nl')" @click="switchLang('en')"><u>NL</u> / EN</b-nav-item>
              <b-nav-item v-else @click="switchLang('nl')">NL / <u>EN</u></b-nav-item>
              <b-nav-item href="https://github.com/lejafar/factrank">
                <icon name="brands/github" />
              </b-nav-item>
            </b-navbar-nav>
          </b-navbar-nav>
        </b-collapse>
      </b-container>
    </b-navbar>
    <div
      class="spacing bg-primary-color"
      v-if="this.$route.name == 'Landing'"
    />
  </div>
</template>

<script>
export default {
  name: "MenuBar",
  methods: {
    resetQuery() {
      this.$router.push({
        query: {},
      });
      this.$router.go();
    },
    switchLang(local) {
        localStorage.lang = local;
        this.$i18n.locale = local;
    },
  },
  mounted() {
    if (localStorage.getItem("lang") === null) {
        localStorage.lang = (navigator.language || navigator.userLanguage).split('-')[0];
    }
    this.$i18n.locale = localStorage.lang;
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar-brand {
  font-size: 40px;
  font-weight: 700;
  font-style: italic;
}

.nav-link,
.navbar-light,
.navbar-brand {
  color: #ffffff !important;
}

#try_it {
  margin-left: 1rem;
}
</style>
