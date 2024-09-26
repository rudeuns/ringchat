import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";

interface CodeProps extends React.HTMLAttributes<HTMLElement> {
  inline?: boolean;
  className?: string;
  children?: React.ReactNode;
}

const MarkdownComponents = {
  h1: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h1
      className="mt-4 text-3xl font-extrabold whitespace-pre-wrap break-words"
      {...props}
    />
  ),
  h2: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h2
      className="mt-4 text-2xl font-bold whitespace-pre-wrap break-words"
      {...props}
    />
  ),
  h3: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h3
      className="mt-4 text-xl font-semibold whitespace-pre-wrap break-words"
      {...props}
    />
  ),
  p: (props: React.HTMLAttributes<HTMLParagraphElement>) => (
    <p
      className="text-base font-normal whitespace-pre-wrap break-words break-all"
      {...props}
    />
  ),
  code: ({ inline, className, children, style, ...props }: CodeProps) => {
    const match = /language-(\w+)/.exec(className || "");

    return !inline && match ? (
      <SyntaxHighlighter {...props} language={match[1]} PreTag="div">
        {String(children).replace(/\n$/, "")}
      </SyntaxHighlighter>
    ) : (
      <code
        className={`inline px-2 py-1 text-primary bg-muted rounded-md`}
        {...props}
      >
        {children}
      </code>
    );
  },
  blockquote: (props: React.BlockquoteHTMLAttributes<HTMLQuoteElement>) => (
    <blockquote
      className="italic ps-4 border-s-4 whitespace-pre-wrap break-words"
      {...props}
    />
  ),
  ul: (props: React.HTMLAttributes<HTMLUListElement>) => (
    <ul
      className="flex flex-col space-y-5 whitespace-pre-wrap break-words"
      {...props}
    />
  ),
  ol: (props: React.OlHTMLAttributes<HTMLOListElement>) => (
    <ol className="flex flex-col whitespace-pre-wrap break-words" {...props} />
  ),
  li: (props: React.LiHTMLAttributes<HTMLLIElement>) => (
    <li className="whitespace-pre-wrap break-words" {...props} />
  ),
  a: (props: React.AnchorHTMLAttributes<HTMLAnchorElement>) => (
    <a className="whitespace-pre-wrap break-words hover:underline" {...props} />
  ),
};

export default function Markdown({ content }: { content?: string }) {
  return (
    <ReactMarkdown className="p-1" components={MarkdownComponents}>
      {content}
    </ReactMarkdown>
  );
}
