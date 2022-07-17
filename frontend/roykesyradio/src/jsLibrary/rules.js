export const rules = {
  required: (value) => !!value || "required",
  username: (v) => {
    return (
      (v != null && v.length >= 6 && v.length <= 30) ||
      "Must be between 6-30 characters"
    );
  },
  nickname: (v) => {
    return (
      (v != null && v.length >= 6 && v.length <= 30) ||
      "Must be between 6-30 characters"
    );
  },
  musicName: (v) => {
    return (
      (v != null && v.length >= 1 && v.length <= 50) ||
      "Must be between 1-50 characters"
    );
  },
  arrayRequired: (v) => {
    return v.length > 0 || "required";
  },
  id: (v) => {
    return (
      (v != null && v.length >= 3 && v.length <= 50) ||
      "Must be between 3-50 characters"
    );
  },
  password: (v) => {
    return (
      (v != null && v.length >= 6 && v.length <= 30) ||
      "Must be between 6-30 characters"
    );
  },
  title: (v) => {
    return (
      (v != null && v.length >= 2 && v.length <= 50) ||
      "Must be between 2-50 characters"
    );
  },
  description: (v) => {
    return (v != null && v.length <= 500) || "Input at most 500 characters";
  },
  cost: (v) => {
    return (
      (v != null && v > 0 && v <= 1000000) ||
      "Please enter a positive integer within 1000000"
    );
  },
  files: (v) => {
    return v.length > 0 || "Please uplaod picture";
  },
  parentClass: (v) => {
    return (
      (v != null && v.length >= 1 && v.length <= 25) ||
      "Must be between 1-25 characters"
    );
  },
  subClass: (v) => {
    return (
      (v != null && v.length >= 1 && v.length <= 25) ||
      "Must be between 1-25 characters"
    );
  },
  buyCount: (v) => {
    return (v != null && v >= 1 && v <= 500) || "Must be between 1-500";
  },
  name: (v) => {
    return (v != null && v.length <= 40) || "Input at most 40 characters";
  },
};
