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
        <q-form @submit="changeName" class="q-gutter-md">
          <q-input
            dense
            outlined
            v-model="profile.full_name"
            type="text"
            label="Full name"
            class="q-my-sm"
          />
          <q-input
            dense
            outlined
            v-model="profile.phone_number"
            type="text"
            label="Phone number"
            class="q-my-sm"
          />
          <q-input
            dense
            outlined
            v-model="profile.address"
            type="text"
            label="Address"
            class="q-my-sm"
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
          />
          <q-input
            dense
            outlined
            v-model="profile.password"
            type="password"
            label="Password"
            class="q-my-sm"
          />
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
      profile: {
        full_name: this.data.full_name,
        phone_number: this.data.phone_number,
        address: this.data.address,
        gender: this.data.gender,
        password: "",
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
    async changeName() {
      let res = await Services.put("api/v1/self/info", this.profile, this);
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
  .btn-close {
    margin: -8px 0px 0px -8px;
  }
}
</style>
