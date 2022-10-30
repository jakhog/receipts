import { lazy, Suspense } from 'react';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import '@fontsource/roboto';

const Layout = lazy(() => import('./Layout'));

const theme = createTheme({
});

export const App = () => {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Suspense fallback={<></>}>
                <Layout />
            </Suspense>
        </ThemeProvider>
    );
};
