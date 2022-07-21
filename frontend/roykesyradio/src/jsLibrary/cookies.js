export function clearUserInformationCookies(_this) {
  let removeKey = ["username", "nickname"];
  delete_cookie("session");
  for (let key of removeKey) {
    if (_this.$cookies.isKey(key)) _this.$cookies.remove(key);
  }
}

function delete_cookie(name) {
  document.cookie = name + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}
