// Cache buster v3 - Final Version

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-control-allow-headers': 'authorization, x-client-info, apikey, content-type, swift-fingerprint',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Luarmor-style gatekeeper check
    const userHwid = req.headers.get('swift-fingerprint')
    if (!userHwid) {
      const accessDeniedHtml = `
        <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Access Denied</title>
        <style>body { background-color: #121212; color: #E0E0E0; font-family: monospace; text-align: center; padding-top: 20%; }</style>
        </head><body><h1>You're not supposed to be here.</h1></body></html>
      `
      return new Response(accessDeniedHtml, { headers: { ...corsHeaders, 'Content-Type': 'text/html' }, status: 403 });
    }

    // Connect to Supabase
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!
    )

    const url = new URL(req.url)
    const userKey = url.searchParams.get('key')

    if (!userKey) {
      return new Response('print("Error: Key not provided.")', { headers: corsHeaders })
    }

    const { data: keyData, error } = await supabase
      .from('keys')
      .select('hwid')
      .eq('key', userKey)
      .single()

    if (error || !keyData) {
      return new Response('print("Error: Invalid Key.")', { headers: corsHeaders })
    }

    // This is the "real script" that will be sent on success
    const Yourscript = `
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!! PUT YOUR SCRIPT HERE FATTY !!!!!!!!!!!!!!!!!!!!!!!!")

    `

    // Main logic
    if (keyData.hwid === null) {
      // FIRST USE: Link HWID and send the script
      await supabase.from('keys').update({ hwid: userHwid }).eq('key', userKey)
      return new Response(Yourscript, { headers: corsHeaders })

    } else if (keyData.hwid === userHwid) {
      // WELCOME BACK: HWID matches, send the script
      return new Response(Yourscript, { headers: corsHeaders })

    } else {
      // HWID MISMATCH
      return new Response('print("Error: This key is already bound to another user.")', { headers: corsHeaders })
    }

  } catch (e) {
    // General server error
    return new Response(`print("Server Error: ${e.message}")`, { headers: corsHeaders, status: 500 })
  }
})
