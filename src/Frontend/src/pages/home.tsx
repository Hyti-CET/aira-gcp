// Copyright 2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import type { NextPage } from 'next'
import { ReactElement, ReactNode, useEffect, useState } from 'react';
import { Layout } from '@/layouts';
import { SCOPE_LEARNER } from '@/constants/rbac';
import { useRouter } from 'next/router';
import { useAuth } from '@/context/auth';

type NextPageWithLayout = NextPage & {
    getLayout?: (page: ReactElement) => ReactNode
}

export default function Home<NextPageWithLayout>() {
    const [mounted, setMounted] = useState<boolean>(false);
    
    const router = useRouter();
    const { user } = useAuth();

    useEffect(() => {
        setMounted(true);

        if (!user || !user.scopes) {
            router.push("/");
            setMounted(false);
        }
            
        const isStudent = user && user.scopes && user.scopes.some(s => [SCOPE_LEARNER].includes(s));
        if (isStudent) router.push("/exams");
        else router.push("/reports");

        return () => setMounted(false);
    }, [user, router])

    if (!mounted) return null;

    return null;
}

Home.getLayout = function getLayout(page: ReactElement) {
    return (
        <Layout>
            {page}
        </Layout>
    );
}

export async function getServerSideProps({ locale } : any) {
    return {
        props: {
            ...(await serverSideTranslations(locale, ['common', 'admin', 'toast', 'routes'])),
        }
    }
}