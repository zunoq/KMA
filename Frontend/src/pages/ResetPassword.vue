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
                  <div class="text-h5 q-pb-xl">Reset your password</div>
                  <div class="row q-col-gutter-sm">
                    <div class="col-12">
                      <q-input
                        dense
                        outlined
                        v-model="reset.email"
                        type="text"
                        label="Email"
                      />
                    </div>
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
                  <div class="text-h5 q-pb-lg">
                    OTP has been sent to your Email
                  </div>

                  <div class="row q-col-gutter-sm">
                    <div class="col-12">
                      <q-input
                        dense
                        outlined
                        v-model="reset.new_password"
                        type="password"
                        label="New password"
                      />
                    </div>
                    <div class="col-12">
                      <q-input
                        dense
                        outlined
                        v-model="confirm"
                        type="password"
                        label="Confirm"
                      />
                    </div>
                    <div class="col-6">
                      <q-input
                        dense
                        outlined
                        v-model="reset.otp"
                        type="text"
                        label="OTP"
                      />
                    </div>
                    <div class="col-6">
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
                        @click="resetPassword"
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
      confirm: "",
      reset: {
        email: "",
        otp: "",
        new_password: "",
      },
    };
  },
  methods: {
    validate() {
      if (this.reset.email == "") {
        Notify.create({
          message: "Please enter first name",
          color: "negative",
          position: "top",
        });
        this.$refs.firstname.focus();
      } else if (this.reset.new_password != this.confirm) {
        Notify.create({
          message: "Password don't match",
          color: "negative",
          position: "top",
        });
        this.reset.new_password = "";
        this.confirm = "";
      } else if (this.reset.otp == "") {
        Notify.create({
          message: "Please enter OTP",
          color: "negative",
          position: "top",
        });
      } else {
        this.isValid = true;
      }
    },
    sendOTP() {
      Loading.show();
      if (this.reset.email != "") {
        this.showResend = false;
        Services.post("/api/v1/otp/reset", {
          email: this.reset.email,
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
    resetPassword() {
      this.validate();
      if (this.isValid == true) {
        console.log(this.newAccount);
        Services.put("/api/v1/password/reset", this.reset).then((res) => {
          console.log(res);
          if (res.status == 200) {
            Notify.create({
              message: "Success",
              position: "top",
              color: "positive",
            });
            this.$router.push("/login");
          } else {
            console.log(res.status.code);
            Notify.create({
              message: res.data.message,
              color: "negative",
              position: "top",
            });
          }
        });
      }
    },
  },

  created() {},
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
