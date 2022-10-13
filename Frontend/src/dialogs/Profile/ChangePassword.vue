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
            v-model="current_password"
            type="password"
            label="Recently password"
            class="q-my-sm"
          />
          <q-input
            dense
            outlined
            v-model="new_password"
            type="password"
            label="New password"
            class="q-my-sm"
          />
          <q-input
            dense
            outlined
            v-model="confirm"
            type="password"
            label="Confirm"
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
              label="Change password"
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
      current_password: "",
      new_password: "",
      confirm: "",
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
      if (this.new_password == this.confirm) {
        let res = await Services.put(
          "api/v1/self/password",
          {
            current_password: this.current_password,
            new_password: this.new_password,
          },
          this
        );
        if (res.status == 200) {
          this.onOKClick();
        }
      } else {
        Notify.create({
          message: "Password don't match",
          color: "negative",
          position: "top",
        });
        (this.new_password = ""),
          (this.current_password = ""),
          (this.confirm = "");
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
