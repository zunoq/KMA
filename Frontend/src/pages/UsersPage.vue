<template>
  <q-page class="q-pa-sm">
    <div class="row q-mb-sm">
      <q-btn
        v-show="role == 'admin'"
        color="primary"
        label="Create new user "
        @click="createStaff()"
        class="q-mr-md"
      />
    </div>
    <q-table
      flat
      bordered
      :title="role == 'admin' ? 'All user' : 'All customer'"
      :rows="users"
      :columns="columns"
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
              {{ props.row.role }}
            </span>
          </q-td>
          <q-td key="username" class="text-center">
            <span class="">
              {{ props.row.username }}
            </span>
          </q-td>
          <q-td key="full_name" class="text-center">
            <span class="">
              {{ props.row.full_name }}
            </span>
          </q-td>
          <q-td key="email" class="text-center">
            <span class="">
              {{ props.row.email }}
            </span>
          </q-td>
          <q-td key="phone_number" class="text-center">
            <span class="">
              {{ props.row.phone_number }}
            </span>
          </q-td>
          <q-td key="address" class="text-center">
            <span class="">
              {{ props.row.address }}
            </span>
          </q-td>
          <q-td key="is_active" class="text-center">
            <span
              class="text-bold text-uppercase"
              :class="props.row.is_active ? 'text-primary' : 'text-negative'"
            >
              {{ props.row.is_active }}
            </span>
          </q-td>
          <q-td key="action" class="text-center">
            <div class="float-right">
              <q-btn
                round
                flat
                color="info"
                icon="edit"
                class="q-mx-sm"
                size="md"
                @click.stop="editUser(props.row)"
              >
                <q-tooltip> Modify </q-tooltip>
              </q-btn>
              <q-btn
                round
                flat
                color="negative"
                icon="delete_forever"
                class="q-mx-sm"
                size="md"
                @click.stop="deleteUser(props.row)"
              >
                <q-tooltip> Delete </q-tooltip>
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
import Services from "src/services/rest.service.js";
import CreateStaff from "src/dialogs/Users/CreateStaff.vue";
import EditStaff from "src/dialogs/Users/EditStaff.vue";
export default defineComponent({
  name: "UsersPage",
  data() {
    return {
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
      role: LocalStorage.getItem("role"),
      users: [],
    };
  },
  methods: {
    async getUsers() {
      let response = await Services.get("/api/v1/users");
      console.log(response);
      this.users = response.users;
    },
    createStaff() {
      this.$q
        .dialog({
          component: CreateStaff,
          componentProps: {},
        })
        .onOk((e) => {
          console.log(e);
          this.getUsers();
        })
        .onCancel(() => {});
    },
    editUser(data) {
      this.$q
        .dialog({
          component: EditStaff,
          componentProps: {
            data: data,
          },
        })
        .onOk((e) => {
          console.log(e);
          this.getUsers();
        })
        .onCancel(() => {});
    },
    async deleteUser(data) {
      let response = await Services.delete(`api/v1/users/${data.id}`);
      this.getUsers();
      if (response.status == 204) {
        Notify.create({
          message: "Success",
          color: "positive",
          position: "top",
        });
      } else {
        Notify.create({
          message: response.data.message,
          color: "negative",
          position: "top",
        });
      }
    },
  },
  mounted() {
    this.getUsers();
  },
});
</script>
