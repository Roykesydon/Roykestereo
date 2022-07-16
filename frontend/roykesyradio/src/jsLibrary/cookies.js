export function clearUserInformationCookies(_this) {
  let removeKey = ["username", "nickname"];
  for (let key of removeKey) {
    if (_this.$cookies.isKey(key)) _this.$cookies.remove(key);
  }
}
