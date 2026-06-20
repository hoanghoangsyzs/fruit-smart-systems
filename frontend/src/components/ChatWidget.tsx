import { FormEvent, useRef, useState } from "react";
import { api, ChatMessage } from "../api";

const WELCOME: ChatMessage = {
  role: "assistant",
  content:
    "Chào bạn, mình là trợ lý Durian Smart. Bạn có thể hỏi về bệnh sầu riêng, độ chín, chất lượng trái, cách chụp ảnh phân tích hoặc cách dùng hệ thống.",
};

const QUICK_PROMPTS = [
  "Những bệnh thường gặp ở sầu riêng?",
  "Cách chụp ảnh sầu riêng để phân tích chính xác?",
  "Điểm chất lượng được tính như thế nào?",
];

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>(QUICK_PROMPTS);
  const inputRef = useRef<HTMLInputElement>(null);

  async function sendMessage(text: string) {
    const clean = text.trim();
    if (!clean || loading) return;

    const nextMessages: ChatMessage[] = [...messages, { role: "user", content: clean }];
    setMessages(nextMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await api.chat(clean, nextMessages.slice(-10));
      setMessages([...nextMessages, { role: "assistant", content: res.reply }]);
      setSuggestions(res.suggestions);
    } catch (err) {
      setMessages([
        ...nextMessages,
        {
          role: "assistant",
          content:
            err instanceof Error
              ? `Mình chưa gửi được câu hỏi: ${err.message}`
              : "Mình chưa gửi được câu hỏi. Bạn thử lại sau nhé.",
        },
      ]);
    } finally {
      setLoading(false);
      window.setTimeout(() => inputRef.current?.focus(), 0);
    }
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage(input);
  }

  return (
    <div className="chat-widget">
      {open && (
        <section className="chat-panel" aria-label="Trợ lý Durian Smart">
          <header className="chat-head">
            <div>
              <strong>Trợ lý Durian Smart</strong>
              <small>Hỗ trợ phân tích và chăm sóc vườn sầu riêng</small>
            </div>
            <button type="button" className="chat-icon-btn" onClick={() => setOpen(false)} aria-label="Đóng chat">
              ×
            </button>
          </header>

          <div className="chat-messages">
            {messages.map((message, index) => (
              <div key={`${message.role}-${index}`} className={`chat-message ${message.role}`}>
                {message.content}
              </div>
            ))}
            {loading && <div className="chat-message assistant">Mình đang suy nghĩ...</div>}
          </div>

          <div className="chat-suggestions">
            {suggestions.slice(0, 3).map((item) => (
              <button key={item} type="button" onClick={() => void sendMessage(item)} disabled={loading}>
                {item}
              </button>
            ))}
          </div>

          <form className="chat-form" onSubmit={onSubmit}>
            <input
              ref={inputRef}
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Nhập câu hỏi..."
              maxLength={1000}
            />
            <button type="submit" disabled={loading || !input.trim()}>
              Gửi
            </button>
          </form>
        </section>
      )}

      <button type="button" className="chat-toggle" onClick={() => setOpen((value) => !value)} aria-label="Mở chat">
        Chat
      </button>
    </div>
  );
}
