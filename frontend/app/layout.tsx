export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'Inter, sans-serif', margin: 0, padding: '1rem 2rem' }}>{children}</body>
    </html>
  );
}
