import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { MantineProvider, createTheme, AppShell, MantineThemeOverride } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import './styles/newspaper.css';
import { AuthProvider } from './presentation/providers/AuthProvider';
import { ProtectedRoute } from './presentation/components/ProtectedRoute';
import { PublicRoute } from './presentation/components/PublicRoute';
import { Header } from './presentation/components/Header';
import { Footer } from './presentation/components/Footer';
import { LoginPage } from './presentation/pages/LoginPage';
import { RegisterPage } from './presentation/pages/RegisterPage';
import { HomePage } from './presentation/pages/HomePage';
import { ProfilePage } from './presentation/pages/ProfilePage';
import { AuthorsPage } from './presentation/pages/AuthorsPage';
import { FeedPage } from './presentation/pages/FeedPage';

// Тема в стиле старой газеты
const newspaperTheme: MantineThemeOverride = createTheme({
  primaryColor: 'yellow',
  fontFamily: '"Times New Roman", "Georgia", "Times", serif',
  headings: {
    fontFamily: '"Times New Roman", "Georgia", "Times", serif',
    fontWeight: '700',
  },
  colors: {
    newspaper: [
      '#fef9e7',
      '#fef5d4',
      '#fef0b8',
      '#fde99c',
      '#fde280',
      '#fcdb64',
      '#fcd448',
      '#d4b23c',
      '#ac9030',
      '#846e24',
    ],
    sepia: [
      '#faf8f3',
      '#f5f0e6',
      '#f0e8d9',
      '#ebe0cc',
      '#e6d8bf',
      '#e1d0b2',
      '#dcc8a5',
      '#b8a789',
      '#94866d',
      '#706551',
    ],
  },
  defaultRadius: 'xs',
  components: {
    Paper: {
      defaultProps: {
        style: {
          backgroundColor: '#fef9e7',
          backgroundImage: `
            repeating-linear-gradient(
              0deg,
              transparent,
              transparent 2px,
              rgba(0,0,0,0.03) 2px,
              rgba(0,0,0,0.03) 4px
            )
          `,
        },
      },
    },
    Button: {
      defaultProps: {
        style: {
          fontFamily: '"Times New Roman", "Georgia", "Times", serif',
        },
      },
    },
    TextInput: {
      defaultProps: {
        style: {
          fontFamily: '"Times New Roman", "Georgia", "Times", serif',
        },
      },
    },
    Textarea: {
      defaultProps: {
        style: {
          fontFamily: '"Times New Roman", "Georgia", "Times", serif',
        },
      },
    },
  },
});

function App() {
  return (
    <MantineProvider theme={newspaperTheme}>
      <Notifications />
      <BrowserRouter>
        <AuthProvider>
          <AppShell
            header={{ height: 60 }}
            footer={{ height: 60 }}
            styles={{
              main: {
                backgroundColor: '#fef9e7',
                backgroundImage: `
                  repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0,0,0,0.02) 2px,
                    rgba(0,0,0,0.02) 4px
                  ),
                  radial-gradient(
                    circle at 20% 50%,
                    rgba(139, 69, 19, 0.1) 0%,
                    transparent 50%
                  ),
                  radial-gradient(
                    circle at 80% 80%,
                    rgba(160, 82, 45, 0.08) 0%,
                    transparent 50%
                  )
                `,
                minHeight: '100vh',
              },
              footer: {
                padding: 0,
                width: '100%',
              },
            }}
          >
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
                <Route
                  path="/authors"
                  element={
                    <ProtectedRoute>
                      <AuthorsPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/feed"
                  element={
                    <ProtectedRoute>
                      <FeedPage />
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

