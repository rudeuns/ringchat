interface InputFieldProps {
  type: string;
  placeholder: string;
  name: string;
  value: string;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function InputField(props: InputFieldProps) {
  return (
    <input 
      className="input-field"
      type={props.type}
      placeholder={props.placeholder}
      name={props.name}
      value={props.value}
      onChange={props.handleChange}
      autoComplete='off'
    />
  )
}