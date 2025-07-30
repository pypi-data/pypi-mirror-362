// Grab the global from the UMD build CRA loaded onto window.ReactRouterDOM
const RR = window.ReactRouterDOM;

// Re-export everything so that `import { Link, useNavigate } from 'react-router-dom'` works.
export default RR;
export const {
  BrowserRouter,
  HashRouter,
  MemoryRouter,
  Routes,
  Route,
  Link,
  NavLink,
  useNavigate,
  useParams,
  useLocation,
  useMatch,
  useResolvedPath,
  // …and any other APIs you need
} = RR;
