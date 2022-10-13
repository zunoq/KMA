<template>
  <q-page class="q-pa-lg">
    <!-- Thông tin cơ bản -->
    <div class="row justify-center">
      <q-card
        class="my-card col-xl-6 col-lg-8 col-md-12 col-sm-12 col-xs-12 q-pl-md"
        flat
        bordered
      >
        <q-card-section>
          <div class="text-h6">Basic information</div>
        </q-card-section>
        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Avatar
            </div>
            <div class="col-7 text-body2 text-layout text-italic">
              Change your avatar
            </div>
            <div class="col-1 text-body1">
              <q-avatar
                size="60px"
                class="cursor-pointer relative-position layout"
              >
                <q-img src="../assets/image/avatar.jpg" :ratio="1">
                  <div class="absolute-bottom edit-avatar">
                    <q-icon name="mdi-camera" size="16px" color="floor" />
                  </div>
                </q-img>
              </q-avatar>
            </div>
          </q-card-section>
          <q-separator />
        </div>
        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Role
            </div>
            <div
              class="col-7 text-title text-secondary text-uppercase text-bold"
            >
              {{ userInfo.role }}
            </div>
            <div class="col-1 text-body1"></div>
          </q-card-section>
          <q-separator />
        </div>
        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Name
            </div>
            <div class="col-7 text-title text-secondary">
              {{ userInfo.full_name }}
            </div>
            <div class="col-1 text-body1">
              <q-btn
                icon="mdi-chevron-right"
                size="sm"
                flat
                @click="changeName"
              />
            </div>
          </q-card-section>
          <q-separator />
        </div>
        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Gender
            </div>
            <div class="col-7 text-title text-secondary text-capitalize">
              {{ userInfo.gender }}
            </div>
            <div class="col-1 text-body1"></div>
          </q-card-section>
          <q-separator />
        </div>

        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Email
            </div>
            <div class="col-7 text-title text-secondary">
              {{ userInfo.email }}
            </div>
            <div class="col-1 text-body1"></div>
          </q-card-section>
          <q-separator />
        </div>

        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Address
            </div>
            <div class="col-7 text-title text-secondary">
              {{ userInfo.address }}
            </div>
            <div class="col-1 text-body1"></div>
          </q-card-section>
          <q-separator />
        </div>
        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Phone
            </div>
            <div class="col-7 text-title text-secondary">
              {{ userInfo.phone_number }}
            </div>
            <div class="col-1 text-body1"></div>
          </q-card-section>
          <q-separator />
        </div>
        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Join date
            </div>
            <div class="col-7 text-title text-secondary">
              {{ dateConvert(userInfo.date_joined) }}
            </div>
            <div class="col-1 text-body1"></div>
          </q-card-section>
          <q-separator />
        </div>
        <div>
          <q-card-section class="row flex flex-center">
            <div class="col-4 text-uppercase text-caption text-layout">
              Password
            </div>
            <div class="col-7 text-body2 text-layout text-italic">
              Change your password
            </div>
            <div class="col-1 text-body1">
              <q-btn
                icon="mdi-chevron-right"
                size="sm"
                flat
                @click="changePassword"
              />
            </div>
          </q-card-section>
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { LocalStorage, Notify } from "quasar";
import ChangeName from "src/dialogs/Profile/ChangeName.vue";
import ChangePassword from "src/dialogs/Profile/ChangePassword.vue";
import Services from "src/services/rest.service.js";
export default defineComponent({
  name: "SettingPage",
  data() {
    return {
      userInfo: {},
    };
  },
  methods: {
    getSelf() {
      Services.get("api/v1/self/info").then((res) => {
        this.userInfo = res;
      });
    },
    changeName() {
      this.$q
        .dialog({
          component: ChangeName,
          componentProps: {
            data: this.userInfo,
          },
        })
        .onOk((e) => {
          console.log(e);
          this.getSelf();
        })
        .onCancel(() => {});
    },
    changePassword() {
      this.$q
        .dialog({
          component: ChangePassword,
          componentProps: {},
        })
        .onOk(() => {
          console.log("OK");
        })
        .onCancel(() => {
          console.log("Cancel");
        })
        .onDismiss(() => {
          console.log("Called on OK or Cancel");
        });
    },
  },
  computed: {
    dateConvert() {
      return (time) => {
        let date = new Date(time);
        let options = {
          year: "numeric",
          month: "long",
          day: "numeric",
        };
        return date.toLocaleString(options);
      };
    },
  },
  watch: {
    userInfo: {
      handler(val) {
        this.userInfo = val;
      },
    },
  },
  mounted() {
    this.getSelf();
  },
});
</script>
<style lang="scss" scoped>
.q-img__content > div {
  padding: 0px 16px;
}
.edit-avatar {
  width: 100%;
  height: 18px;
  text-align: center;
}
</style>
