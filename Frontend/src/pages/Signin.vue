<template>
  <q-page padding class="flex flex-center">
    <div>
      <q-card outline class="login-card" flat bordered>
        <q-btn
          v-show="step == 2"
          flat
          round
          color="secondary"
          icon="mdi-arrow-left"
          class="absolute btn-back"
          @click="$refs.stepper.previous()"
        />
        <q-img
          src="../assets/image/logo.png"
          :ratio="1"
          height="40px"
          fit="contain"
        />
        <q-stepper
          v-model="step"
          ref="stepper"
          animated
          contracted
          header-class="hidden"
          flat
        >
          <q-step
            :name="1"
            :done="step > 1"
            title="STEP 1"
            header-class="hidden"
          >
            <div class="step step-1">
              <q-card class="" flat>
                <q-card-section>
                  <div class="text-h6 text-center title">Login</div>
                  <div class="text-subtitle1 text-center text-secondary">
                    Login to continue
                  </div>
                </q-card-section>
                <q-card-section>
                  <q-input
                    outlined
                    ref="username"
                    v-model="account.username"
                    label="Username"
                    :error="notValid"
                    @blur="validateUsername()"
                    @keyup.enter="
                      validateUsername();
                      checkUsername();
                    "
                  />
                </q-card-section>
                <q-card-actions align="left">
                  <q-btn
                    @click="this.$router.push('/resetpassword')"
                    no-caps
                    flat
                    color="primary"
                    label="Forgot password?"
                  />
                </q-card-actions>
              </q-card>
            </div>
          </q-step>

          <q-step :name="2" :done="step > 2" title="STEP 2">
            <q-card class="step step-2" flat>
              <q-card-section>
                <div class="text-h6 text-center title">Welcome</div>
                <div class="text-subtitle1 text-center text-secondary">
                  {{ account.username }}
                </div>
              </q-card-section>
              <q-card-section>
                <q-input
                  outlined
                  ref="password"
                  v-model="account.password"
                  label="Password"
                  :type="showPassword ? 'text' : 'password'"
                  :error="notValid"
                  @blur="validatePassword"
                  @keyup.enter="
                    validatePassword();
                    checkPassword();
                  "
                />
                <q-checkbox v-model="showPassword" label="Show password" />
              </q-card-section>
            </q-card>
          </q-step>
          <template v-slot:navigation>
            <q-stepper-navigation>
              <div class="row justify-between step-nav">
                <q-btn
                  v-if="step == 1"
                  @click="createAccount"
                  label="Create account"
                  class="col-auto"
                  no-caps
                  color="primary"
                  flat
                />
                <q-btn
                  v-if="step == 2"
                  no-caps
                  @click="this.$router.push('/resetpassword')"
                  label="Forgot password?"
                  class="col-auto"
                  color="primary"
                  flat
                />
                <q-btn
                  v-if="step == 1"
                  @click="checkUsername"
                  color="primary"
                  label="Continue"
                  no-caps
                  class="col-auto"
                />
                <q-btn
                  v-if="step == 2"
                  @click="checkPassword"
                  label="Login"
                  color="primary"
                  no-caps
                  class="col-auto"
                />
              </div>
            </q-stepper-navigation>
          </template>
        </q-stepper>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { LocalStorage, Notify, Loading } from "quasar";
import Services from "src/services/user.service.js";
import Rest from "src/services/rest.service.js";
export default defineComponent({
  name: "ProfilePage",
  data() {
    return {
      step: ref(1),
      notValid: ref(),
      showPassword: ref(false),
      account: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    validateUsername() {
      if (this.account.username.length == 0) {
        this.notValid = true;
        Notify.create({
          message: "Please enter username",
          color: "negative",
          position: "top",
        });
      } else {
        this.notValid = false;
      }
    },
    checkUsername() {
      if (this.notValid == false) {
        this.$refs.stepper.next();
        this.notValid = ref();
      } else {
        Notify.create({
          message: "Please enter username",
          color: "negative",
          position: "top",
        });
      }
    },
    validatePassword() {
      if (this.account.password.length == 0) {
        this.notValid = true;
        Notify.create({
          message: "Please enter password",
          color: "negative",
          position: "top",
        });
      } else {
        this.notValid = false;
      }
    },
    checkPassword() {
      if (this.notValid == false) {
        Loading.show({
          spinnerColor: "white",
        });
        try {
          Services.login(this.account).then(() => {
            if (localStorage.getItem("token")) {
              Loading.hide();
              Rest.get("/api/v1/self/info").then((res) => {
                LocalStorage.set("role", res.role);
                console.log("setted");
              });
              this.$router.push("/profile");
            } else {
              Loading.hide();
              this.$q.notify({
                type: "negative",
                message: "Username or password is incorrect",
                position: "top",
              });
              this.$refs.stepper.previous();
              this.account.username = "";
              this.account.password = "";
            }
          });
        } catch (err) {}
      } else {
        Notify.create({
          message: "Please enter password",
          color: "negative",
          position: "top",
        });
      }
    },
    createAccount() {
      this.$router.push("/signup");
    },
  },
});
</script>
<style lang="scss" scoped>
.login-card {
  min-width: 448px;
  height: auto;
  min-height: 472px;
  padding: 48px 16px 36px;
  .q-stepper--horizontal {
    padding: 0px;
    .step {
      min-height: 268px;
      .q-card__section--vert {
        padding: 16px 0px;
      }
      .q-card__actions {
        padding: 16px 0px;
        align-items: center;
      }
    }
    .step-1 {
      .q-btn--flat {
        margin-left: -8px;
      }
    }
    .step-2 {
      .q-checkbox {
        margin-left: -8px;
      }
    }
  }
  .step-nav {
    .q-btn--flat {
      margin-left: -16px;
    }
  }
  .btn-back {
    top: 8px;
    left: 8px;
  }
}
</style>
