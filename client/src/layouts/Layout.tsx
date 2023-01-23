import { Outlet, Navigate } from "react-router-dom";
import Header from "components/Header";
import Footer from "components/Footer";

export default function Layout() {
  const isLoggedIn = localStorage.getItem("signed_in");

  // Save path for redirect after login
  if (!isLoggedIn) {
    localStorage.setItem(
      "redirect",
      window.location.href.replace(window.location.origin, ""),
    );
  }

  return isLoggedIn ? (
    <>
      <Header />

      <main>
        <Outlet />
      </main>

      <Footer />
    </>
  ) : (
    <Navigate to="/login" replace />
  );
}
