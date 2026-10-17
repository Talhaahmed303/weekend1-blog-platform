import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'FalconXoft Blog Platform | Engineering MVP',
  description: 'Multi-Author Publishing Platform with Role-Based Access Control, Draft/Publish Workflows, Categories, and Real-time Search.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased selection:bg-sky-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
