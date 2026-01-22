import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { useEffect } from "react";
import ScrollToTop from "@/components/ui/ScrollToTop";
import Index from "./pages/Index";
import Prediction from "./pages/prediction";
import PlayerStatistics from "./pages/PlayerStatistics"
import Statistics from "./pages/Statistics";
import PipelinePage from "./pages/workflow";   
import TestCrests from "./pages/TestCrests";
import NotFound from "./pages/prediction";
import KnowClubs from "./pages/knowclubs";
import Contact from "./pages/Contact";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <ScrollToTop />
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/statistics" element={<Statistics />} />
          <Route path="/statistics/match/players" element={<PlayerStatistics />} />
          <Route path="/workflow" element={<PipelinePage />} />
          <Route path="/test-crests" element={<TestCrests />} />
          <Route path="/knowclubs" element={<KnowClubs />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
