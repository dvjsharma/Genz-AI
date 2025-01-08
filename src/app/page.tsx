import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, BarChart2, MessageCircle, Instagram } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-400 via-purple-500 to-cyan-500 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Navigation */}
        <nav className="rounded-2xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-lg mb-12">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-xl font-bold text-white">
                  InstaIQ
                </span>
              </div>
              <div className="flex space-x-4">
                <Button variant="ghost" className="text-white hover:bg-white/20">About</Button>
                <Link href="/chat">
                  <Button className="bg-white/20 hover:bg-white/30 backdrop-blur-lg text-white border border-white/20">
                    Try Now
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="rounded-3xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-lg p-12 mb-12">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h1 className="text-5xl font-bold text-white leading-tight">
                Analyze Your Social Media Content
              </h1>
              <p className="text-xl text-white/80">
                Get AI-powered insights about your Instagram content and engagement
              </p>
              <Link href="/chat">
                <br/>
                <Button className="bg-white/20 hover:bg-white/30 backdrop-blur-lg text-white border border-white/20 px-8 py-6 text-lg">
                  Start Analyzing <ArrowRight className="ml-2" />
                </Button>
              </Link>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full blur-3xl opacity-30"></div>
              <div className="relative aspect-square rounded-3xl backdrop-blur-xl bg-white/10 border border-white/20 p-8 flex items-center justify-center">
                <Instagram className="w-32 h-32 text-white opacity-80" />
              </div>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: <Instagram className="w-6 h-6" />,
              title: "Connect Instagram",
              description: "Optionally connect your Instagram account for personalized insights"
            },
            {
              icon: <MessageCircle className="w-6 h-6" />,
              title: "Chat with AI",
              description: "Ask questions and get instant insights about social media content"
            },
            {
              icon: <BarChart2 className="w-6 h-6" />,
              title: "Get Analytics",
              description: "Receive detailed analytics and recommendations for improvement"
            }
          ].map((feature, i) => (
            <div key={i} className="rounded-2xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-lg p-6 hover:bg-white/20 transition-all">
              <div className="bg-white/10 w-12 h-12 rounded-xl flex items-center justify-center mb-4 backdrop-blur-xl">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">{feature.title}</h3>
              <p className="text-white/80">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

