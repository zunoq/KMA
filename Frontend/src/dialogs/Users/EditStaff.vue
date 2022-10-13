<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin text-regular text-page">
      <q-card-section>
        <div class="align-right">
          <q-btn
            flat
            round
            icon="mdi-window-close"
            class="btn-close"
            @click="hide"
          />
        </div>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 text-center text-bold">Edit user</div>
      </q-card-section>
      <q-card-section>
        <q-form @submit="editStaff" class="">
          <div class="row q-col-gutter-md q-mb-lg">
            <q-input
              dense
              outlined
              v-model="profile.username"
              type="text"
              label="Username"
              class="col-12"
            />
            <q-select
              dense
              outlined
              v-model="profile.role"
              :options="roleOptions"
              borderless
              emit-value
              map-options
              label="Role"
              class="col-6"
            />
            <q-select
              dense
              outlined
              v-model="profile.is_active"
              :options="activeOptions"
              borderless
              emit-value
              map-options
              label="Is active?"
              class="col-6"
            />
            <q-input
              dense
              outlined
              v-model="profile.password"
              type="password"
              label="Password"
              class="col-6"
            />
            <q-input
              dense
              outlined
              v-model="profile.confirm_password"
              type="password"
              label="Confirm password"
              class="col-6"
            />
            <div class="col-12">
              <q-separator spaced inset />
            </div>
            <q-input
              dense
              outlined
              v-model="profile.full_name"
              type="text"
              label="Full name"
              class="col-8"
            />
            <q-select
              dense
              outlined
              v-model="profile.gender"
              :options="genderOptions"
              borderless
              emit-value
              map-options
              label="Gender"
              class="col-4"
            />
            <q-input
              dense
              outlined
              v-model="profile.email"
              type="text"
              label="Email"
              class="col-6"
            />
            <q-input
              dense
              outlined
              v-model="profile.phone_number"
              type="text"
              label="Phone number"
              class="col-6"
            />
            <q-input
              dense
              outlined
              v-model="profile.address"
              type="text"
              label="Address"
              class="col-12"
            />
          </div>
          <div class="flex flex-center">
            <q-btn
              no-caps
              outline
              type="submit"
              class="text-bold"
              color="primary"
              icon="manage_accounts"
              label="Update"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from "vue";
import Services from "src/services/rest.service.js";
import { useDialogPluginComponent, Notify } from "quasar";
export default {
  props: {
    data: Object,
  },
  emits: [
    // REQUIRED; need to specify some events that your
    // component will emit through useDialogPluginComponent()
    ...useDialogPluginComponent.emits,
  ],
  data() {
    return {
      genderOptions: [
        { value: "male", label: "Male" },
        { value: "female", label: "Female" },
      ],
      roleOptions: [
        { value: "admin", label: "Admin" },
        { value: "staff", label: "Staff" },
        { value: "customer", label: "Customer" },
      ],
      activeOptions: [
        { value: true, label: "True" },
        { value: false, label: "False" },
      ],
      profile: {
        full_name: this.data.full_name,
        email: this.data.email,
        address: this.data.address,
        gender: this.data.gender,
        phone_number: this.data.phone_number,
        username: this.data.username,
        password: this.data.password,
        confirm_password: this.data.confirm_password,
        role: "",
        is_active: this.data.is_active,
      },
    };
  },
  setup() {
    // REQUIRED; must be called inside of setup()
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();
    // dialogRef      - Vue ref to be applied to QDialog
    // onDialogHide   - Function to be used as handler for @hide on QDialog
    // onDialogOK     - Function to call to settle dialog with "ok" outcome
    //                    example: onDialogOK() - no payload
    //                    example: onDialogOK({ /*.../* }) - with payload
    // onDialogCancel - Function to call to settle dialog with "cancel" outcome

    return {
      // This is REQUIRED;
      // Need to inject these (from useDialogPluginComponent() call)
      // into the vue scope for the vue html template
      dialogRef,
      onDialogHide,

      // other methods that we used in our vue html template;
      // these are part of our example (so not required)
      onOKClick() {
        // on OK, it is REQUIRED to
        // call onDialogOK (with optional payload)
        onDialogOK();
        // or with payload: onDialogOK({ ... })
        // ...and it will also hide the dialog automatically
      },

      // we can passthrough onDialogCancel directly
      onCancelClick: onDialogCancel,
    };
  },
  methods: {
    async editStaff() {
      console.log(this.profile);
      let res = await Services.put(
        `/api/v1/users/${this.data.id}`,
        this.profile,
        this
      );
      console.log(res);
      if (res.status == 200) {
        this.onOKClick();
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.q-dialog-plugin {
  width: 600px;
  .btn-close {
    margin: -8px 0px 0px -8px;
  }
}
</style>
