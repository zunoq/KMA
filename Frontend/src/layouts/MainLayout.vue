<template>
  <q-layout view="hHh lpR fFf">
    <q-drawer show-if-above side="left" bordered :width="250">
      <q-item clickable class="row" @click="this.$router.push('/profile')">
        <div class="col-auto">
          <q-avatar size="56px" class="q-mr-md">
            <img src="../assets/image/avatar.jpg" />
          </q-avatar>
        </div>
        <div class="col-auto max-height text-secondary q-mt-sm">
          <div class="text-weight-bold">
            {{ self.full_name }}
          </div>
          <div>
            <span class="text-uppercase text-caption text-info text-bold">
              {{ self.role }}
            </span>
          </div>
        </div>
      </q-item>
      <q-separator />
      <div>
        <div class="fit column justify-between">
          <q-list>
            <template v-for="(menuItem, idx) in leftPanel" :key="idx">
              <q-item
                clickable
                active-class="active-page"
                :to="menuItem.direct"
                class="full-state"
              >
                <q-item-section avatar class="column q-py-xs">
                  <q-icon color="secondary" :name="menuItem.icon" size="28px" />
                </q-item-section>

                <q-item-section class="text-secondary text-title">
                  {{ menuItem.label }}
                </q-item-section>
              </q-item>
            </template>
          </q-list>
        </div>
      </div>
      <q-btn
        flat
        class="absolute-bottom q-ma-md"
        color="negative"
        label="Sign out"
        @click="signOut()"
      />
    </q-drawer>

    <q-page-container>
      <router-view class="text-regular bg-floor" />
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref } from "vue";
import { LocalStorage } from "quasar";
import restServices from "src/services/rest.service.js";
import userServices from "src/services/user.service.js";
export default {
  data() {
    return {
      leftPanel: [
        {
          icon: "home",
          label: "Home",
          direct: "/home",
        },
        {
          icon: "poll",
          label: "Survey",
          direct: "/survey",
        },
        {
          icon: "manage_accounts",
          label: "Users manage",
          direct: "/users",
          role: "admin",
        },
      ],
      self: {},
    };
  },
  methods: {
    async getSelf() {
      let response = await restServices.get("/api/v1/self/info");
      this.self = response;
      LocalStorage.set("role", this.self.role);
    },
    signOut() {
      userServices.logout();
    },
  },
  watch: {
    self: {
      handler(val) {
        LocalStorage.set("role", val.role);
      },
    },
  },
  created() {
    this.getSelf();
  },
};
</script>
