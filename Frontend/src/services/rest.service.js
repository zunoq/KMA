import { api } from "boot/axios";
import UserService from "./user.service";
import { LocalStorage, Notify } from "quasar";

function authHeader() {
  var token = LocalStorage.getItem("token");
  if (token) {
    return {
      Authorization: "Bearer " + token.access,
      "Content-Type": "application/json",
    };
  } else {
    return {};
  }
}
const token = LocalStorage.getItem("token");

class RESTService {
  async get(link, params = {}, thisComponent = undefined) {
    try {
      if (Object.keys(params).length > 0)
        var response = await api.get(link, { params, headers: authHeader() });
      else var response = await api.get(link, { headers: authHeader() });
      if (thisComponent) {
        Notify.create({
          message: "Thành công",
          color: "positive",
          position: "top",
        });
      }
      return response.data;
    } catch (error) {
      if (error.response) {
        if (error.response.status == 401) {
          Notify.create({
            message: "Chưa đang nhập vào hệ thống",
            color: "negative",
            position: "top",
          });
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        } else {
          if (error.response.status == 403) {
            Notify.create({
              message: "Không có quyền thực thi",
              color: "negative",
              position: "top",
            });
          } else {
            if (error.response.status >= 500) {
              Notify.create({
                message: "Lỗi hệ thống",
                color: "negative",
                position: "top",
              });
              // window.location.href = "/system-error";
            } else {
              if (error.response.status == 404) {
                Notify.create({
                  message: "Lỗi không tìm thấy trang",
                  color: "negative",
                  position: "top",
                });
                // window.location.href = "/notfound";
              } else {
                if (error.response.status == 423) {
                  Notify.create({
                    message: "Biểu mẫu đã ngừng hoạt động",
                    color: "negative",
                    position: "top",
                  });
                  return error.response.data;
                } else {
                  return error.response;
                }
              }
            }
          }
        }
      } else {
        if (error) {
          if (error.message === "Network Error") {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/network-error";
          } else {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/system-error";
          }
        } else {
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        }
      }
    }
  }

  async post(link, body, thisComponent = undefined) {
    try {
      var response = await api.post(link, body, { headers: authHeader() });
      if (thisComponent) {
        Notify.create({
          message: "Success",
          color: "positive",
          position: "top",
        });
      }
      return response;
    } catch (error) {
      if (error.response) {
        if (error.response.status == 401) {
          Notify.create({
            message: "Chưa đang nhập vào hệ thống",
            color: "negative",
            position: "top",
          });
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        } else {
          if (error.response.status == 403) {
            Notify.create({
              message: "Không có quyền thực thi",
              color: "negative",
              position: "top",
            });
          } else {
            if (error.response.status >= 500) {
              Notify.create({
                message: "Lỗi hệ thống",
                color: "negative",
                position: "top",
              });
              // window.location.href = "/system-error";
            } else {
              if (error.response.status == 404) {
                Notify.create({
                  message: "Lỗi không tìm thấy trang",
                  color: "negative",
                  position: "top",
                });
                // window.location.href = "/notfound";
              } else {
                if (error.response.status == 406) {
                  Notify.create({
                    message: "Đã gửi quá số lần cho phép",
                    color: "negative",
                    position: "top",
                  });
                } else {
                  return error.response;
                }
              }
            }
          }
        }
      } else {
        if (error) {
          if (error.message === "Network Error") {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/network-error";
          } else {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/system-error";
          }
        } else {
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        }
      }
    }
  }

  async put(link, body, thisComponent = undefined) {
    try {
      var response = await api.put(link, body, { headers: authHeader() });
      if (thisComponent) {
        Notify.create({
          message: "Success",
          color: "positive",
          position: "top",
        });
      }
      return response;
    } catch (error) {
      if (error.response) {
        if (error.response.status == 401) {
          Notify.create({
            message: "Chưa đang nhập vào hệ thống",
            color: "negative",
            position: "top",
          });
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        } else {
          if (error.response.status == 403) {
            Notify.create({
              message: "Không có quyền thực thi",
              color: "negative",
              position: "top",
            });
          } else {
            if (error.response.status >= 500) {
              Notify.create({
                message: "Lỗi hệ thống",
                color: "negative",
                position: "top",
              });
              // window.location.href = "/system-error";
            } else {
              if (error.response.status == 404) {
                Notify.create({
                  message: "Lỗi không tìm thấy trang",
                  color: "negative",
                  position: "top",
                });
                // window.location.href = "/notfound";
              } else {
                return error.response;
              }
            }
          }
        }
      } else {
        if (error) {
          if (error.message === "Network Error") {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/network-error";
          } else {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/system-error";
          }
        } else {
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        }
      }
    }
  }
  async delete(link, thisComponent = undefined) {
    try {
      var response = await api.delete(link, { headers: authHeader() });
      if (thisComponent) {
        Notify.create({
          message: "Success",
          color: "positive",
          position: "top",
        });
      }
      return response.data;
    } catch (error) {
      if (error.response) {
        if (error.response.status == 401) {
          Notify.create({
            message: "Chưa đang nhập vào hệ thống",
            color: "negative",
            position: "top",
          });
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        } else {
          if (error.response.status == 403) {
            Notify.create({
              message: "Không có quyền thực thi",
              color: "negative",
              position: "top",
            });
          } else {
            if (error.response.status >= 500) {
              Notify.create({
                message: "Lỗi hệ thống",
                color: "negative",
                position: "top",
              });
              // window.location.href = "/system-error";
            } else {
              if (error.response.status == 404) {
                Notify.create({
                  message: "Lỗi không tìm thấy trang",
                  color: "negative",
                  position: "top",
                });
                // window.location.href = "/notfound";
              } else {
                return error.response;
              }
            }
          }
        }
      } else {
        if (error) {
          if (error.message === "Network Error") {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/network-error";
          } else {
            Notify.create({
              message: error.message,
              color: "negative",
              position: "top",
            });
            // window.location.href = "/system-error";
          }
        } else {
          if (token) {
            UserService.logout(token.refresh);
          } else {
            UserService.logout();
            // window.location.href = "/login";
          }
        }
      }
    }
  }
}

export default new RESTService();
