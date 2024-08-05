interface InputFieldProps {
  type: string;
  placeholder: string;
}

export default function InputField(props: InputFieldProps) {
  return (
    <input 
      className="input-field"
      type={props.type}
      placeholder={props.placeholder}
    />
  )
}