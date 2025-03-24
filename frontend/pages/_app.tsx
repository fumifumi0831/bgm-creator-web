import '../styles/globals.css';
import type { AppProps } from 'next/app';
import Head from 'next/head';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>BGM Creator Web</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="Create YouTube BGM videos easily" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
