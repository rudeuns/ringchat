import { StylesConfig } from "react-select";
import {
  HiOutlineStar,
  HiOutlineLink,
  HiOutlineBookmark,
} from "react-icons/hi2";

export const selectOptions = [
  {
    label: (
      <div className="container-select-option">
        <HiOutlineStar className="icon-base" />
        <p className="ms-select-option">별점 높은 순</p>
      </div>
    ),
  },
  {
    label: (
      <div className="container-select-option">
        <HiOutlineLink className="icon-base" />
        <p className="ms-select-option">첨부 많은 순</p>
      </div>
    ),
  },
  {
    label: (
      <div className="container-select-option">
        <HiOutlineBookmark className="icon-base" />
        <p className="ms-select-option">저장 많은 순</p>
      </div>
    ),
  },
];

export const selectStyles: StylesConfig<any, false> = {
  control: (provided) => ({
    ...provided,
    cursor: "pointer",
    color: "var(--color-black)",
    borderColor: "var(--color-muted)",
    boxShadow: "none",
    "&:hover": {
      borderColor: "none",
      boxShadow: "none",
    },
  }),
  menu: (provided) => ({
    ...provided,
    backgroundColor: "var(--color-white)",
    boxShadow: "1px 1px 4px 1px var(--color-gray)",
  }),
  option: (provided, state) => ({
    ...provided,
    cursor: "pointer",
    color: state.isFocused ? "var(--color-white)" : "var(--color-black)",
    backgroundColor: state.isFocused ? "var(--color-primary-light)" : "none",
    "&:active": {
      backgroundColor: "var(--color-primary-light)",
    },
  }),
};
