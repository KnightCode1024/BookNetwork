import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { MantineProvider, createTheme, AppShell } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import { AuthProvider } from './presentation/providers/AuthProvider';
import { ProtectedRoute } from './presentation/components/ProtectedRoute';
import { PublicRoute } from './presentation/components/PublicRoute';
import { Header } from './presentation/components/Header';
import { Footer } from './presentation/components/Footer';
import { LoginPage } from './presentation/pages/LoginPage';
import { RegisterPage } from './presentation/pages/RegisterPage';
import { HomePage } from './presentation/pages/HomePage';
import { ProfilePage } from './presentation/pages/ProfilePage';

const theme = createTheme({});

function App() {
  return (
    <MantineProvider theme={theme}>
      <Notifications />
      <BrowserRouter>
        <AuthProvider>
          <AppShell header={{ height: 60 }} footer={{ height: 60 }}>
            <AppShell.Header>
              <Header />
            </AppShell.Header>
            <AppShell.Main>
              <Routes>
                <Route
                  path="/login"
                  element={
                    <PublicRoute>
                      <LoginPage />
                    </PublicRoute>
                  }
                />
                <Route
                  path="/register"
                  element={
                    <PublicRoute>
                      <RegisterPage />
                    </PublicRoute>
                  }
                />
                <Route
                  path="/"
                  element={
                    <ProtectedRoute>
                      <HomePage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <ProfilePage />
                    </ProtectedRoute>
                  }
                />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AppShell.Main>
            <AppShell.Footer>
              <Footer />
            </AppShell.Footer>
          </AppShell>
        </AuthProvider>
      </BrowserRouter>
    </MantineProvider>
  );
}

export default App;

