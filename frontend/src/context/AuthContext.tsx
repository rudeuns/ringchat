'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface User {
  email: string;
  name: string;
}

interface AuthContextType {
  isAuth: boolean;
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
  testLogin: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  
  const [isAuth, setIsAuth] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  const login = (user: User) => {
    // TODO: get token logic
    localStorage.setItem("token", "...");
    setUser(user);
    setIsAuth(true)
    router.push('/chat');
  };

  const testLogin = () => {
    localStorage.setItem("token", "dummytoken");
    localStorage.setItem("user", JSON.stringify({email: "example@gmail.com", name: "example"}));
    setUser({email: "example@gmail.com", name: "example"} as User);
    setIsAuth(true)
    router.push('/chat');
  }

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setIsAuth(false);
    router.push('/');
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      setIsAuth(true);
      setUser(JSON.parse(user));
      
      if (pathname === '/') {
        router.push('/chat')
      }
    } else {
      setIsAuth(false)
      router.push('/')
    }
  }, [pathname]);

  return (
    <AuthContext.Provider value={{ isAuth, user, login, logout, testLogin }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
