<template>
  <q-page class="flex flex-center">
    <div>
      <q-card class="my-card q-pa-lg" flat bordered>
        <div class="row">
          <div class="col-7">
            <div class="row">
              <div class="text-h6 text-bold col-12">
                <span class="text-primary"> Vu Long </span>
              </div>
            </div>
            <div class="row">
              <q-stepper
                v-model="step"
                color="primary"
                animated
                flat
                header-class="hidden"
                class="full-width my-stepper"
              >
                <q-step
                  :name="1"
                  title="Select campaign settings"
                  icon="settings"
                  :done="step > 1"
                >
                  <div class="text-h5 q-pb-xl">
                    Create an account
                  </div>
                  <div class="row q-col-gutter-sm">
                    <div class="col-6">
                      <q-input
                        dense
                        outlined
                        v-model="newAccount.first_name"
                        type="text"
                        label="First name"
                      />
                    </div>
                    <div class="col-6">
                      <q-input
                        dense
                        outlined
                        v-model="newAccount.last_name"
                        type="text"
                        label="Last name"
                      />
                    </div>
                    <div class="col-12">
                      <q-input
                        dense
                        outlined
                        v-model="newAccount.email"
                        type="text"
                        label="Email"
                      />
                      <div class="text-caption text-grey q-pb-md q-pt-sm">
                        Each email can signup one account
                      </div>
                    </div>
                    <div class="col-6">
                      <q-input
                        dense
                        outlined
                        v-model="newAccount.password"
                        :type="showPassword ? 'text' : 'password'"
                        label="Password"
                      />
                    </div>
                    <div class="col-6">
                      <q-input
                        dense
                        outlined
                        v-model="newAccount.confirmPassword"
                        :type="showPassword ? 'text' : 'password'"
                        label="Confirm"
                      />
                    </div>
                    <div class="col-12">
                      <div class="text-caption text-grey q-pb-md q-pt-sm">
                        Use 6 or more characters with a mix of letters, numbers
                        & symbols
                      </div>
                    </div>
                    <q-checkbox
                      v-model="showPassword"
                      label="Show password"
                      dense
                    />
                  </div>

                  <q-stepper-navigation>
                    <div class="justify-between flex">
                      <q-btn
                        @click="this.$router.push('/signin')"
                        color="primary"
                        label="Sign in"
                        no-caps
                        style="margin-left: -16px"
                        flat
                      />
                      <q-btn
                        @click="sendOTP"
                        color="primary"
                        label="Continue"
                        no-caps
                      />
                    </div>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="2"
                  title="Create an ad group"
                  caption="Optional"
                  icon="create_new_folder"
                  :done="step > 2"
                >
                  <div class="text-h5 q-pb-lg">Verify your Email</div>
                  <div class="text-caption q-pb-md">
                    For your security, VAP wants to make sure it's really you.
                    VAP will send a email with a 6-digit verification code.
                  </div>
                  <div class="row">
                    <div class="col-6">
                      <q-input
                        dense
                        outlined
                        v-model="newAccount.otp"
                        type="text"
                        label="OTP"
                      />
                    </div>
                    <div class="q-ml-md col-6">
                      <q-btn
                        v-show="showResend"
                        @click="sendOTP"
                        color="primary"
                        label="Resend"
                        no-caps
                        icon="send"
                        flat
                      />
                    </div>
                  </div>
                  <q-stepper-navigation>
                    <div class="justify-between flex">
                      <q-btn
                        @click="this.step = 1"
                        color="negative"
                        label="Back"
                        no-caps
                        style="margin-left: -16px"
                        flat
                      />
                      <q-btn
                        @click="createAccount"
                        color="primary"
                        label="Continue"
                        no-caps
                      />
                    </div>
                  </q-stepper-navigation>
                </q-step>
              </q-stepper>
            </div>
          </div>
          <div class="col-5 flex flex-center">
            <q-img src="../assets/image/account.png" alt="" fit />
          </div>
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { Notify, LocalStorage, Loading } from "quasar";
import Services from "src/services/rest.service.js";
export default defineComponent({
  name: "IndexPage",
  data() {
    return {
      showResend: ref(false),
      step: ref(1),
      isValid: ref(false),
      showPassword: ref(false),
      newAccount: {
        first_name: "",
        last_name: "",
        email: "",
        otp: "",
        password: "",
        confirmPassword: "",
      },
    };
  },
  methods: {
    validate() {
      if (this.newAccount.first_name == "") {
        Notify.create({
          message: "Please enter first name",
          color: "negative",
        });
        this.$refs.firstname.focus();
      } else if (this.newAccount.last_name == "") {
        Notify.create({
          message: "Please enter last name",
          color: "negative",
        });
        this.$refs.lastname.focus();
      } else if (this.newAccount.email == "") {
        Notify.create({
          message: "Please enter email",
          color: "negative",
        });
        this.$refs.email.focus();
      } else if (this.newAccount.password.length < 6) {
        Notify.create({
          message: "Password must at least 6 charactor",
          color: "warning",
        });
        this.newAccount.password = "";
        this.newAccount.confirmPassword = "";
        this.$refs.password.focus();
      } else if (
        this.newAccount.password != "" &&
        this.newAccount.password != this.newAccount.confirmPassword
      ) {
        Notify.create({
          message: "Password don't match, try again",
          color: "negative",
        });
        this.newAccount.password = "";
        this.newAccount.confirmPassword = "";
        this.$refs.password.focus();
      } else {
        this.isValid = true;
      }
    },
    sendOTP() {
      Loading.show();
      if (this.newAccount.email != "") {
        this.showResend = false;
        Services.post("api/v1/otp/send", {
          email: this.newAccount.email,
        }).then((res) => {
          Loading.hide();
          this.step = 2;
          setTimeout(() => {
            this.showResend = true;
          }, 30000);
          console.log(res);
        });
      } else {
        Notify.create({
          message: "Email is not valid",
          color: "negative",
          position: "top",
        });
      }
    },
    createAccount() {
      this.validate();
      if (this.isValid == true) {
        console.log(this.newAccount);
        Services.post("/api/v1/private/users", this.newAccount)
          .then((res) => {
            console.log(res);
            if (res.code == 200) {
              this.$router.push("/login");
            } else {
              console.log(res.status.code);
            }
          })
          .catch((error) => {
            Notify.create({
              message: error.status.code,
              color: "negative",
              position: "top",
            });
          });
      }
    },
  },
  
  created() {
  },
});
</script>

<style lang="scss" scoped>
.my-card {
  width: 768px;
  height: 550px;
}
.my-stepper {
  margin-left: -24px !important;
}
</style>
