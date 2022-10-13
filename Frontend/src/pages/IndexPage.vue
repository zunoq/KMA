<template>
  <q-page class="q-pa-sm">
    <q-btn
      color="primary"
      label="Create customer"
      v-if="role == 'staff'"
      class="q-mb-sm"
      @click="createCustomer"
    />

    <q-table
      flat
      bordered
      title="User Request"
      :rows="staffRequest"
      :columns="role == 'admin' ? columns : columns_staff"
      :pagination="pagination"
      row-key="name"
      hide-pagination
      table-header-class="text-uppercase text-bold text-primary"
      class="text-body1"
    >
      <template #body="props">
        <q-tr :props="props" class="cursor-pointer text-title">
          <q-td key="role" class="text-center">
            <span class="text-title text-uppercase text-bold">
              {{ props.row.data.role }}
            </span>
          </q-td>
          <q-td key="username" class="text-center">
            <span class="">
              {{ props.row.data.username }}
            </span>
          </q-td>
          <q-td key="full_name" class="text-center">
            <span class="">
              {{ props.row.data.full_name }}
            </span>
          </q-td>
          <q-td key="email" class="text-center">
            <span class="">
              {{ props.row.data.email }}
            </span>
          </q-td>
          <q-td key="phone_number" class="text-center">
            <span class="">
              {{ props.row.data.phone_number }}
            </span>
          </q-td>
          <q-td key="address" class="text-center">
            <span class="">
              {{ props.row.data.address }}
            </span>
          </q-td>
          <q-td key="is_active" class="text-center">
            <span
              class="text-bold text-uppercase"
              :class="
                props.row.data.is_active ? 'text-primary' : 'text-negative'
              "
            >
              {{ props.row.data.is_active }}
            </span>
          </q-td>
          <q-td key="status" class="text-center" v-if="role == 'staff'">
            <span class="text-capitalize text-bold">
              {{ props.row.status }}
            </span>
          </q-td>
          <q-td key="action" class="text-center">
            <div class="float-right" v-if="role == 'admin'">
              <q-btn
                round
                flat
                color="positive"
                icon="done"
                class="q-mx-sm"
                size="md"
                @click.stop="staffApprove(props.row)"
              >
                <q-tooltip> Approve </q-tooltip>
              </q-btn>
              <q-btn
                round
                flat
                color="warning"
                icon="block"
                class="q-mx-sm"
                size="md"
                @click.stop="staffReject(props.row)"
              >
                <q-tooltip> Reject </q-tooltip>
              </q-btn>
              <q-btn
                round
                flat
                color="negative"
                icon="delete_forever"
                class="q-mx-sm"
                size="md"
                @click.stop="deleteRequest(props.row)"
              >
                <q-tooltip> Delete </q-tooltip>
              </q-btn>
            </div>
            <div class="float-right" v-if="role == 'staff'">
              <q-btn
                round
                flat
                color="negative"
                icon="close"
                class="q-mx-sm"
                size="md"
                @click.stop="requestCancel(props.row.id)"
              >
                <q-tooltip> Cancel </q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { LocalStorage, Notify } from "quasar";
import Services from "src/services/rest.service";
import CreateCustomer from "src/dialogs/Home/CreateCustomer.vue";
export default defineComponent({
  name: "IndexPage",
  data() {
    return {
      role: LocalStorage.getItem("role"),
      pagination: {
        page: 1,
        rowsPerPage: 0,
      },
      columns: [
        {
          name: "role",
          required: true,
          align: "center",
          label: "Role",
          field: (row) => row.role,
          sortable: true,
        },
        {
          name: "username",
          required: true,
          align: "center",
          label: "Username",
          field: (row) => row.username,
          sortable: true,
        },

        {
          name: "full_name",
          required: true,
          align: "center",
          label: "Name",
          field: (row) => row.full_name,
          sortable: true,
        },
        {
          name: "email",
          required: true,
          align: "center",
          label: "Email",
          field: (row) => row.email,
          sortable: true,
        },
        {
          name: "phone_number",
          required: true,
          align: "center",
          label: "Phone number",
          field: (row) => row.phone_number,
          sortable: true,
        },
        {
          name: "address",
          required: true,
          align: "center",
          label: "Address",
          field: (row) => row.address,
          sortable: true,
        },
        {
          name: "is_active",
          required: true,
          align: "center",
          label: "Active",
          field: (row) => row.is_active,
          sortable: true,
        },
        {
          name: "action",
          required: true,
          label: "",
          align: "right",
          sortable: false,
        },
      ],
      columns_staff: [
        {
          name: "role",
          required: true,
          align: "center",
          label: "Role",
          field: (row) => row.role,
          sortable: true,
        },
        {
          name: "username",
          required: true,
          align: "center",
          label: "Username",
          field: (row) => row.username,
          sortable: true,
        },

        {
          name: "full_name",
          required: true,
          align: "center",
          label: "Name",
          field: (row) => row.full_name,
          sortable: true,
        },
        {
          name: "email",
          required: true,
          align: "center",
          label: "Email",
          field: (row) => row.email,
          sortable: true,
        },
        {
          name: "phone_number",
          required: true,
          align: "center",
          label: "Phone number",
          field: (row) => row.phone_number,
          sortable: true,
        },
        {
          name: "address",
          required: true,
          align: "center",
          label: "Address",
          field: (row) => row.address,
          sortable: true,
        },
        {
          name: "is_active",
          required: true,
          align: "center",
          label: "Active",
          field: (row) => row.is_active,
          sortable: true,
        },
        {
          name: "status",
          required: true,
          align: "center",
          label: "Status",
          field: (row) => row.status,
          sortable: true,
        },
        {
          name: "action",
          required: true,
          label: "",
          align: "right",
          sortable: false,
        },
      ],

      staffRequest: [],
    };
  },
  methods: {
    // ADMIN

    async getStaffRequest() {
      let response = await Services.get(`/api/v1/staff/requests`);
      console.log(response);
      this.staffRequest = response.requests;
    },
    async staffApprove(data) {
      let response = await Services.put(`api/v1/staff/requests/${data.id}`, {
        status: "approved",
      });
      console.log(response);
      if (response.status == 200) {
        Notify.create({
          message: "Success",
          color: "positive",
          position: "top",
        });
        Services.delete(`api/v1/staff/requests/${data.id}`);
        this.getStaffRequest();
      }
    },
    async staffReject(data) {
      let response = await Services.put(`api/v1/staff/requests/${data.id}`, {
        status: "rejected",
      });
      console.log(response);
      if (response.status == 200) {
        Notify.create({
          message: "Success",
          color: "positive",
          position: "top",
        });
        this.getStaffRequest();
      }
    },
    async deleteRequest(data) {
      let response = await Services.delete(`api/v1/staff/requests/${data.id}`);
      console.log(response);
      this.getStaffRequest();
      if (response.status == 204) {
        Notify.create({
          message: "Success",
          color: "positive",
          position: "top",
        });
        this.getStaffRequest();
      }
    },

    // STAFF

    createCustomer() {
      this.$q
        .dialog({
          component: CreateCustomer,
          componentProps: {},
        })
        .onOk((e) => {
          console.log(e);
          this.getStaffRequest();
        })
        .onCancel(() => {});
    },
    requestCancel() {

    }
  },
  mounted() {
    this.getStaffRequest();
  },
});
</script>
